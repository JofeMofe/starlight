class_name SoulDog
extends CharacterBody2D
## Der Seelenhund (§7.2): folgt Klio per Navigation, setzt sich, wenn sie
## steht, kommt auf Zuruf, lässt sich streicheln und trägt die Fee auf dem Rücken.

const CONFIG: MovementConfig = preload("res://data/config/movement.tres")
const SFX_BARK: AudioStream = preload("res://assets/audio/sfx/dog_bark.ogg")
const SFX_PET: AudioStream = preload("res://assets/audio/sfx/pet_happy.ogg")
const SFX_STEPS: Array[AudioStream] = [
	preload("res://assets/audio/sfx/step_grass_1.ogg"),
	preload("res://assets/audio/sfx/step_grass_3.ogg"),
]
const REPATH_INTERVAL: float = 0.25
const PET_TIME: float = 1.3
const COME_ARRIVE_DISTANCE: float = 22.0
## Sitzplatz der Fee je Ansicht (relativ zu den Pfoten)
const SEATS: Dictionary = {"side": Vector2(3, -8), "down": Vector2(0, -9), "up": Vector2(0, -8)}

@export var dog_name: String = "Funke"

var state: StateMachine = StateMachine.new()
var view: String = "side"
var flip: bool = false
var rider: Klio = null

var _target: Node2D = null
var _repath: float = 0.0
var _idle_time: float = 0.0

@onready var _sprite: Sprite2D = $Sprite
@onready var _anim: SheetAnimator = $Anim
@onready var _agent: NavigationAgent2D = $Agent
@onready var _interact: Interactable = $Interactable
@onready var _hearts: CPUParticles2D = $Hearts


func _ready() -> void:
	add_to_group(&"soul_dog")
	collision_layer = PhysicsLayers.ANIMALS
	collision_mask = PhysicsLayers.GROUND_MASK
	_interact.prompt_provider = _prompts
	_interact.interacted.connect(_on_interacted)
	_anim.frame_changed.connect(_on_frame)
	state.add(&"follow", _update_follow)
	state.add(&"sit", _update_sit, _enter_sit)
	state.add(&"come", _update_come)
	state.add(&"petted", _update_petted, _enter_petted)
	state.add(&"ridden", _update_ridden)
	state.transition(&"follow")


func _physics_process(delta: float) -> void:
	if _target == null:
		_target = get_tree().get_first_node_in_group(&"player") as Node2D
	state.update(delta)
	_update_anim()


# --- Zustände ---------------------------------------------------------------

func _update_follow(delta: float) -> void:
	if _target == null:
		return
	var dist: float = global_position.distance_to(_target.global_position)
	if dist > CONFIG.dog_follow_distance:
		var speed: float = CONFIG.dog_run_speed if dist > CONFIG.dog_run_distance else CONFIG.dog_walk_speed
		_steer_towards(_target.global_position, speed, delta)
		_idle_time = 0.0
	else:
		velocity = velocity.move_toward(Vector2.ZERO, CONFIG.dog_accel * delta)
		_face(_target.global_position - global_position)
		_idle_time += delta
		if _idle_time > CONFIG.dog_sit_delay:
			state.transition(&"sit")
	move_and_slide()


func _enter_sit() -> void:
	velocity = Vector2.ZERO


func _update_sit(_delta: float) -> void:
	if _target != null and global_position.distance_to(_target.global_position) > CONFIG.dog_follow_distance + 14.0:
		_idle_time = 0.0
		state.transition(&"follow")


func _update_come(delta: float) -> void:
	if _target == null:
		state.transition(&"follow")
		return
	var dist: float = global_position.distance_to(_target.global_position)
	if dist <= COME_ARRIVE_DISTANCE:
		velocity = Vector2.ZERO
		_face(_target.global_position - global_position)
		_celebrate()
		return
	_steer_towards(_target.global_position, CONFIG.dog_run_speed, delta)
	move_and_slide()


func _enter_petted() -> void:
	velocity = Vector2.ZERO
	_hearts.restart()
	_hearts.emitting = true
	AudioManager.play_sfx(SFX_PET)
	AudioManager.play_sfx(SFX_BARK, -6.0, 0.08, &"SFX", 1.12)
	EventBus.animal_bond_changed.emit(&"soul_dog", 1.0)


func _update_petted(_delta: float) -> void:
	if state.time_in_state >= PET_TIME:
		state.transition(&"sit")


func _update_ridden(delta: float) -> void:
	if rider == null:
		state.transition(&"follow")
		return
	var input: Vector2 = rider.ride_input
	var rate: float = CONFIG.dog_ridden_accel
	velocity = velocity.move_toward(input * CONFIG.dog_ridden_speed, rate * delta)
	move_and_slide()
	if input.length() > 0.2:
		_face(input)
	var seat: Vector2 = SEATS[view] as Vector2
	if view == "side" and flip:
		seat.x = -seat.x
	seat.y += _anim.frame_value("bob")
	rider.sync_to_mount(global_position, seat, view, flip, view == "down",
		velocity.length() / CONFIG.dog_ridden_speed)


# --- Von Klio aufgerufen ----------------------------------------------------

func call_to(caller: Node2D) -> void:
	if state.is_in(&"ridden"):
		return
	_target = caller
	_repath = 0.0
	state.transition(&"come")


func can_dismount() -> bool:
	return true


func clear_rider() -> void:
	rider = null
	state.transition(&"sit")


# --- Intern -----------------------------------------------------------------

func _prompts(actor: Node2D) -> Dictionary:
	var klio: Klio = actor as Klio
	if klio == null or state.is_in(&"ridden"):
		return {"primary": "", "secondary": ""}
	return {"primary": "prompt.dog.ride" if klio.is_fairy else "prompt.pet", "secondary": ""}


func _on_interacted(actor: Node2D) -> void:
	var klio: Klio = actor as Klio
	if klio == null:
		return
	if klio.is_fairy:
		rider = klio
		klio.start_riding(self, &"dog")
		AudioManager.play_sfx(SFX_BARK, -4.0, 0.05, &"SFX", 1.2)
		state.transition(&"ridden")
	else:
		_face(klio.global_position - global_position)
		state.transition(&"petted")


func _celebrate() -> void:
	AudioManager.play_sfx(SFX_BARK)
	state.transition(&"petted")


func _steer_towards(point: Vector2, speed: float, delta: float) -> void:
	_repath -= delta
	if _repath <= 0.0:
		_agent.target_position = point
		_repath = REPATH_INTERVAL
	var next: Vector2 = _agent.get_next_path_position()
	var dir: Vector2 = (next - global_position)
	if dir.length() < 0.5:
		dir = point - global_position
	dir = dir.normalized()
	velocity = velocity.move_toward(dir * speed, CONFIG.dog_accel * delta)
	_face(velocity)


func _face(dir: Vector2) -> void:
	if dir.length() < 1.0:
		return
	if absf(dir.x) > absf(dir.y) * 0.9:
		view = "side"
		flip = dir.x > 0.0
	else:
		view = "down" if dir.y > 0.0 else "up"
	_sprite.flip_h = flip if view == "side" else false


func _update_anim() -> void:
	var speed: float = velocity.length()
	var anim: String
	if state.is_in(&"sit") or state.is_in(&"petted"):
		anim = "sit_"
	elif speed > CONFIG.dog_walk_speed + 12.0:
		anim = "run_"
	elif speed > 6.0:
		anim = "walk_"
	else:
		anim = "idle_"
	var full: StringName = StringName(anim + view)
	if _anim.current != full:
		if _anim.current.begins_with(anim):
			_anim.play_keep_phase(full)
		else:
			_anim.play(full)
	_anim.speed_scale = clampf(speed / CONFIG.dog_walk_speed, 0.7, 1.6) if anim == "walk_" else 1.0


func _on_frame(frame_index: int) -> void:
	if (_anim.current.begins_with("run") or _anim.current.begins_with("walk")) and frame_index % 3 == 0:
		AudioManager.play_sfx(SFX_STEPS[frame_index % 2], -10.0, 0.12, &"SFX", 1.4)
