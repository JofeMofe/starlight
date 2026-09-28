class_name Horse
extends CharacterBody2D
## Pferd (§7.1) für den M1-Prototyp: streicheln, per Pfiff rufen, reiten in
## drei Gangarten mit trägem An-/Abbremsen, Wendekreis und Sprung im Galopp.

const CONFIG: MovementConfig = preload("res://data/config/movement.tres")
const SFX_SNORT: AudioStream = preload("res://assets/audio/sfx/horse_snort.ogg")
const SFX_PET: AudioStream = preload("res://assets/audio/sfx/pet_happy.ogg")
const SFX_GAIT: AudioStream = preload("res://assets/audio/sfx/gait_up.ogg")
const SFX_HOOVES: Array[AudioStream] = [
	preload("res://assets/audio/sfx/hoof_grass_1.ogg"),
	preload("res://assets/audio/sfx/hoof_grass_2.ogg"),
	preload("res://assets/audio/sfx/hoof_grass_3.ogg"),
]
## Hufschlag-Frames je Gangart (Viertakt, Zweitakt, Dreitakt)
const HOOF_FRAMES: Dictionary = {"walk": [0, 2, 4, 6], "trot": [0, 4], "canter": [0, 3, 5]}
const GAIT_KEYS: Array[String] = ["", "gait.walk", "gait.trot", "gait.canter"]
## Sitzplatz des Reiters (relativ zu den Hufen) je Ansicht
const SEATS: Dictionary = {"side": Vector2(-3, -22), "down": Vector2(0, -21), "up": Vector2(0, -19)}
const JUMP_PROBE: Vector2 = Vector2(28, 10)
const PET_TIME: float = 1.4
## Hufe liegen im 96x64-Frame auf Zeile 61 -> Sprite so versetzen, dass sie auf dem Ursprung stehen
const SPRITE_OFFSET_Y: float = -29.0

@export var horse_name: String = "Holunder"

var state: StateMachine = StateMachine.new()
var gait: HorseGait
var view: String = "side"
var flip: bool = false
var rider: Klio = null
var jumping: bool = false

var _jump_t: float = 0.0
var _come_target: Node2D = null
var _last_gait: int = 0

@onready var _sprite: Sprite2D = $Sprite
@onready var _anim: SheetAnimator = $Anim
@onready var _agent: NavigationAgent2D = $Agent
@onready var _interact: Interactable = $Interactable
@onready var _hearts: CPUParticles2D = $Hearts
@onready var _dust: CPUParticles2D = $Dust
@onready var _shadow: Sprite2D = $Shadow


func _ready() -> void:
	add_to_group(&"horses")
	collision_layer = PhysicsLayers.ANIMALS
	collision_mask = PhysicsLayers.GROUND_MASK
	gait = HorseGait.new(CONFIG)
	_interact.prompt_provider = _prompts
	_interact.interacted.connect(_on_pet)
	_interact.interacted_secondary.connect(_on_mount)
	_anim.frame_changed.connect(_on_frame)
	state.add(&"idle", _update_idle, _enter_idle)
	state.add(&"come", _update_come)
	state.add(&"petted", _update_petted, _enter_petted)
	state.add(&"ridden", _update_ridden)
	state.transition(&"idle")


func _physics_process(delta: float) -> void:
	state.update(delta)
	_update_anim()


# --- Zustände ---------------------------------------------------------------

func _enter_idle() -> void:
	velocity = Vector2.ZERO
	gait.speed = 0.0
	gait.gait = HorseGait.Gait.HALT


func _update_idle(_delta: float) -> void:
	pass


func _update_come(delta: float) -> void:
	if _come_target == null:
		state.transition(&"idle")
		return
	var dist: float = global_position.distance_to(_come_target.global_position)
	if dist < 40.0 or state.time_in_state > 12.0:
		state.transition(&"idle")
		_face(_come_target.global_position - global_position)
		AudioManager.play_sfx(SFX_SNORT, -4.0)
		return
	_agent.target_position = _come_target.global_position
	var next: Vector2 = _agent.get_next_path_position()
	var dir: Vector2 = (next - global_position).normalized()
	velocity = velocity.move_toward(dir * CONFIG.horse_come_speed, CONFIG.horse_accel * delta)
	gait.heading = velocity.normalized() if velocity.length() > 1.0 else gait.heading
	gait.speed = velocity.length()
	gait.gait = HorseGait.Gait.TROT if gait.speed > CONFIG.horse_walk_speed + 10.0 else HorseGait.Gait.WALK
	_face(velocity)
	move_and_slide()


func _enter_petted() -> void:
	velocity = Vector2.ZERO
	_hearts.restart()
	_hearts.emitting = true
	AudioManager.play_sfx(SFX_PET)
	AudioManager.play_sfx(SFX_SNORT, -2.0, 0.06)
	EventBus.animal_bond_changed.emit(StringName(horse_name.to_lower()), 1.0)


func _update_petted(_delta: float) -> void:
	if state.time_in_state >= PET_TIME:
		state.transition(&"idle")


func _update_ridden(delta: float) -> void:
	if rider == null:
		state.transition(&"idle")
		return
	gait.step(rider.ride_input, delta)
	velocity = gait.velocity()
	if jumping:
		_jump_t += delta
		if _jump_t >= CONFIG.horse_jump_duration:
			jumping = false
			collision_mask = PhysicsLayers.GROUND_MASK
			_dust.restart()
			_dust.emitting = true
	var before: Vector2 = global_position
	move_and_slide()
	# Gegen ein Hindernis geritten: Tempo passt sich an (kein Durchrutschen)
	if get_slide_collision_count() > 0 and delta > 0.0:
		var moved: float = global_position.distance_to(before) / delta
		gait.speed = minf(gait.speed, moved + 20.0)
	if gait.speed > 1.0:
		_face(gait.heading)
	if int(gait.gait) != _last_gait:
		_last_gait = int(gait.gait)
		rider.gait_changed.emit(GAIT_KEYS[_last_gait])
	var seat: Vector2 = SEATS[view] as Vector2
	if view == "side" and flip:
		seat.x = -seat.x
	seat.y += _anim.frame_value("bob") - _jump_offset()
	rider.sync_to_mount(global_position, seat, view, flip, view == "down",
		gait.speed / CONFIG.horse_canter_speed)


# --- Von Klio aufgerufen ----------------------------------------------------

func whistle_to(caller: Node2D) -> void:
	if state.is_in(&"ridden"):
		return
	_come_target = caller
	state.transition(&"come")


func rider_faster() -> void:
	if jumping:
		return
	var want_jump: bool = gait.request_faster()
	if want_jump:
		_try_jump()
	else:
		AudioManager.play_sfx(SFX_GAIT, -4.0)


func can_dismount() -> bool:
	return gait.speed < 6.0 and not jumping


func clear_rider() -> void:
	rider = null
	rider_changed()
	state.transition(&"idle")


func rider_changed() -> void:
	_last_gait = 0


# --- Intern -----------------------------------------------------------------

func _prompts(actor: Node2D) -> Dictionary:
	var klio: Klio = actor as Klio
	if klio == null or state.is_in(&"ridden"):
		return {"primary": "", "secondary": ""}
	return {"primary": "prompt.pet", "secondary": "" if klio.is_fairy else "prompt.horse.mount"}


func _on_pet(actor: Node2D) -> void:
	_face(actor.global_position - global_position)
	state.transition(&"petted")


func _on_mount(actor: Node2D) -> void:
	var klio: Klio = actor as Klio
	if klio == null or klio.is_fairy:
		return
	rider = klio
	gait.gait = HorseGait.Gait.HALT
	gait.speed = 0.0
	gait.heading = _facing_vector()
	_last_gait = 0
	klio.start_riding(self, &"horse")
	klio.gait_changed.emit("gait.halt")
	AudioManager.play_sfx(SFX_SNORT, -6.0)
	state.transition(&"ridden")


func _try_jump() -> void:
	# Nur springen, wenn die Landestelle frei ist (sonst weigert es sich sanft)
	var landing: Vector2 = global_position + gait.heading * gait.speed * CONFIG.horse_jump_duration
	var shape: RectangleShape2D = RectangleShape2D.new()
	shape.size = JUMP_PROBE
	var q: PhysicsShapeQueryParameters2D = PhysicsShapeQueryParameters2D.new()
	q.shape = shape
	q.transform = Transform2D(0.0, landing + Vector2(0, -JUMP_PROBE.y * 0.5))
	q.collision_mask = PhysicsLayers.GROUND_MASK
	q.exclude = [get_rid()]
	if not get_world_2d().direct_space_state.intersect_shape(q, 1).is_empty():
		AudioManager.play_sfx(SFX_SNORT, -3.0)
		rider.toast_requested.emit("hint.horse.refuse")
		return
	jumping = true
	_jump_t = 0.0
	collision_mask = PhysicsLayers.FLYING_MASK
	AudioManager.play_sfx(SFX_GAIT, -1.0, 0.0, &"SFX", 0.8)


func _jump_offset() -> float:
	if not jumping:
		return 0.0
	return roundf(sin(PI * _jump_t / CONFIG.horse_jump_duration) * CONFIG.horse_jump_height)


func _facing_vector() -> Vector2:
	match view:
		"down":
			return Vector2.DOWN
		"up":
			return Vector2.UP
	return Vector2.RIGHT if flip else Vector2.LEFT


func _face(dir: Vector2) -> void:
	if dir.length() < 0.5:
		return
	if absf(dir.x) > absf(dir.y) * 0.9:
		view = "side"
		flip = dir.x > 0.0
	else:
		view = "down" if dir.y > 0.0 else "up"
	_sprite.flip_h = flip if view == "side" else false


func _update_anim() -> void:
	var gname: StringName = gait.anim_name()
	var full: StringName = StringName(String(gname) + "_" + view)
	if _anim.current != full:
		if String(_anim.current).get_slice("_", 0) == String(gname):
			_anim.play_keep_phase(full)
		else:
			_anim.play(full)
	var target: float = gait.target_speed_for(gait.gait)
	_anim.speed_scale = clampf(gait.speed / target, 0.5, 1.3) if target > 0.0 else 1.0
	_sprite.offset.y = SPRITE_OFFSET_Y - _jump_offset()
	_shadow.modulate.a = 0.3 - _jump_offset() * 0.012


func _on_frame(frame_index: int) -> void:
	var gname: String = String(_anim.current).get_slice("_", 0)
	if HOOF_FRAMES.has(gname) and frame_index in (HOOF_FRAMES[gname] as Array) and not jumping:
		AudioManager.play_sfx(SFX_HOOVES[frame_index % SFX_HOOVES.size()], -3.0, 0.1)
