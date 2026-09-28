class_name Klio
extends CharacterBody2D
## Die Heldin. Zustände: Menschengröße, Feengröße, Verwandlung, Reiten (Pferd),
## Reiten (Hund, nur als Fee). Alle Zahlen kommen aus MovementConfig.

signal prompt_changed(primary: String, secondary: String)
signal toast_requested(text_key: String)
signal camera_punch_requested(direction: Vector2)
signal size_changed(is_fairy: bool)
signal flight_energy_changed(ratio: float, visible: bool)
@warning_ignore("unused_signal")
signal gait_changed(gait_key: String)  # wird vom Reittier ausgelöst

const CONFIG: MovementConfig = preload("res://data/config/movement.tres")

const SFX_TO_FAIRY: AudioStream = preload("res://assets/audio/sfx/transform_to_fairy.ogg")
const SFX_TO_HUMAN: AudioStream = preload("res://assets/audio/sfx/transform_to_human.ogg")
const SFX_BLOCKED: AudioStream = preload("res://assets/audio/sfx/transform_blocked.ogg")
const SFX_STEPS: Array[AudioStream] = [
	preload("res://assets/audio/sfx/step_grass_1.ogg"),
	preload("res://assets/audio/sfx/step_grass_2.ogg"),
	preload("res://assets/audio/sfx/step_grass_3.ogg"),
]
const SFX_WING: AudioStream = preload("res://assets/audio/sfx/wing_flap.ogg")
const SFX_CALL_DOG: AudioStream = preload("res://assets/audio/sfx/call_dog.ogg")
const SFX_WHISTLE: AudioStream = preload("res://assets/audio/sfx/whistle_horse.ogg")
const SFX_MOUNT: AudioStream = preload("res://assets/audio/sfx/mount.ogg")

const HUMAN_SHAPE_SIZE: Vector2 = Vector2(12, 6)
const FAIRY_SHAPE_SIZE: Vector2 = Vector2(6, 4)
const INTERACT_REACH: float = 14.0
const HAIR_STIFFNESS: float = 90.0
const HAIR_DAMPING: float = 9.0
const WOBBLE_TIME: float = 0.3
const FAIRY_RING_RADII: Vector2 = Vector2(34, 18)

@export var input_enabled: bool = true

var state: StateMachine = StateMachine.new()
var is_fairy: bool = false
var facing: Vector2 = Vector2.DOWN
var view: String = "down"
var flight: FlightEnergy
var flying: bool = false
var focus: Interactable = null
var mount: Node2D = null
## Von außen lesbar für Pferd/Hund beim Reiten
var ride_input: Vector2 = Vector2.ZERO

var _fly_height: float = 0.0
var _time: float = 0.0
var _hair_pos: float = 0.0
var _hair_vel: float = 0.0
var _wobble: float = 0.0
var _transform_to_fairy: bool = false
var _transform_swapped: bool = false
var _last_prompt: Array[String] = ["", ""]
var _step_index: int = 0
var _hair_target_override: float = 0.0

@onready var _collision: CollisionShape2D = $Collision
@onready var _shadow: Sprite2D = $Shadow
@onready var _visual: Node2D = $Visual
@onready var _human: Node2D = $Visual/Human
@onready var _body: Sprite2D = $Visual/Human/Body
@onready var _tail: Sprite2D = $Visual/Human/Tail
@onready var _body_anim: SheetAnimator = $Visual/Human/BodyAnim
@onready var _tail_anim: SheetAnimator = $Visual/Human/TailAnim
@onready var _fairy: Node2D = $Visual/Fairy
@onready var _fairy_body: Sprite2D = $Visual/Fairy/FairyBody
@onready var _fairy_anim: SheetAnimator = $Visual/Fairy/FairyAnim
@onready var _wings: Sprite2D = $Visual/Fairy/Wings
@onready var _wings_anim: SheetAnimator = $Visual/Fairy/WingsAnim
@onready var _flash: Sprite2D = $Flash
@onready var _burst: CPUParticles2D = $TransformBurst
@onready var _trail: CPUParticles2D = $FairyTrail
@onready var _sensor: Area2D = $InteractSensor
@onready var _shadow_human: Texture2D = preload("res://assets/sprites/fx/shadow_medium.png")
@onready var _shadow_fairy: Texture2D = preload("res://assets/sprites/fx/shadow_small.png")


func _ready() -> void:
	add_to_group(&"player")
	collision_layer = PhysicsLayers.PLAYER
	flight = FlightEnergy.new(CONFIG.flight_energy_max, CONFIG.flight_drain_per_second,
		CONFIG.flight_regen_per_second, CONFIG.flight_regen_delay)
	_sensor.collision_layer = 0
	_sensor.collision_mask = PhysicsLayers.INTERACT
	_body_anim.frame_changed.connect(_on_body_frame)
	_wings_anim.frame_changed.connect(_on_wing_frame)
	state.add(&"human", _update_human, _enter_human)
	state.add(&"fairy", _update_fairy, _enter_fairy)
	state.add(&"transforming", _update_transforming)
	state.add(&"ride_horse", _update_ride)
	state.add(&"ride_dog", _update_ride)
	var data: PlayerData = GameState.local_player()
	is_fairy = data.is_fairy
	_apply_size_visuals()
	state.transition(&"fairy" if is_fairy else &"human")


func _physics_process(delta: float) -> void:
	_time += delta
	state.update(delta)
	_update_hair(delta)
	_update_visual_offsets(delta)
	_update_focus()


# --- Zustände ---------------------------------------------------------------

func _enter_human() -> void:
	flying = false
	collision_mask = PhysicsLayers.GROUND_MASK
	flight_energy_changed.emit(flight.ratio(), false)


func _enter_fairy() -> void:
	collision_mask = PhysicsLayers.GROUND_MASK
	flight_energy_changed.emit(flight.ratio(), true)


func _update_human(delta: float) -> void:
	var input: Vector2 = _move_input()
	_accelerate(input * CONFIG.human_speed, CONFIG.human_accel, CONFIG.human_friction, delta)
	move_and_slide()
	_update_facing(input)
	var moving: bool = velocity.length() > 8.0
	_body_anim.speed_scale = clampf(velocity.length() / CONFIG.human_speed, 0.6, 1.2) if moving else 1.0
	_play_body(("walk_" if moving else "idle_") + view)
	_handle_common_actions()


func _update_fairy(delta: float) -> void:
	var input: Vector2 = _move_input()
	var wants_fly: bool = input_enabled and Input.is_action_pressed(&"fly_jump") and _secondary_prompt() == ""
	if wants_fly and not flight.is_empty():
		flying = flight.use(delta) or _over_low_obstacle()
	elif flying and _over_low_obstacle():
		# Nie über Zaun/Wasser "abstürzen": weiter schweben, bis der Boden frei ist
		flying = true
	else:
		flying = false
		flight.rest(delta)
	collision_mask = PhysicsLayers.FLYING_MASK if flying else PhysicsLayers.GROUND_MASK
	var speed: float = CONFIG.fairy_fly_speed if flying else CONFIG.fairy_speed
	_accelerate(input * speed, CONFIG.fairy_accel, CONFIG.fairy_friction, delta)
	move_and_slide()
	_update_facing(input)
	_fly_height = move_toward(_fly_height, CONFIG.fly_height if flying else 0.0, 60.0 * delta)
	_wings_anim.speed_scale = 1.7 if flying else (1.2 if velocity.length() > 8.0 else 0.8)
	_trail.emitting = velocity.length() > 20.0
	flight_energy_changed.emit(flight.ratio(), true)
	_handle_common_actions()


func _update_transforming(delta: float) -> void:
	velocity = velocity.move_toward(Vector2.ZERO, CONFIG.human_friction * delta)
	move_and_slide()
	var t: float = state.time_in_state
	# Flackern zwischen beiden Gestalten (pixelgenau, ohne Skalierung)
	var flicker_on: bool = t > 0.08 and t < 0.32 and int(t / 0.04) % 2 == 0
	var show_fairy: bool = (_transform_to_fairy == _transform_swapped)
	_human.visible = not show_fairy if not flicker_on else show_fairy
	_fairy.visible = show_fairy if not flicker_on else not show_fairy
	var peak: float = 1.0 - absf(t - CONFIG.transform_swap_time) / CONFIG.transform_swap_time
	_flash.visible = peak > 0.0
	_flash.modulate.a = clampf(peak, 0.0, 1.0)
	if not _transform_swapped and t >= CONFIG.transform_swap_time:
		_transform_swapped = true
		is_fairy = _transform_to_fairy
		GameState.local_player().is_fairy = is_fairy
		_apply_size_visuals()
		size_changed.emit(is_fairy)
		EventBus.player_size_changed.emit(GameState.LOCAL_PLAYER_ID, is_fairy)
	if t >= CONFIG.transform_duration:
		_flash.visible = false
		_human.visible = not is_fairy
		_fairy.visible = is_fairy
		state.transition(&"fairy" if is_fairy else &"human")


func _update_ride(_delta: float) -> void:
	ride_input = _move_input()
	if not input_enabled or mount == null:
		return
	if Input.is_action_just_pressed(&"fly_jump") and mount.has_method(&"rider_faster"):
		mount.call(&"rider_faster")
	if Input.is_action_just_pressed(&"interact"):
		try_dismount()
	if Input.is_action_just_pressed(&"size_toggle"):
		toast_requested.emit("hint.transform.riding")


# --- Aktionen ---------------------------------------------------------------

func _handle_common_actions() -> void:
	if not input_enabled:
		return
	if Input.is_action_just_pressed(&"size_toggle"):
		try_toggle_size()
	elif Input.is_action_just_pressed(&"interact") and focus != null:
		focus.interact(self)
	elif Input.is_action_just_pressed(&"fly_jump") and focus != null and _secondary_prompt() != "":
		focus.interact_secondary(self)
	elif Input.is_action_just_pressed(&"dog_call"):
		call_dog()
	elif Input.is_action_just_pressed(&"whistle"):
		whistle_horse()


## Größenwechsel versuchen (§6.3). Gibt true zurück, wenn die Verwandlung startet.
func try_toggle_size() -> bool:
	if state.is_in(&"transforming"):
		return false
	if state.is_in(&"ride_horse") or state.is_in(&"ride_dog"):
		toast_requested.emit("hint.transform.riding")
		return false
	var data: PlayerData = GameState.local_player()
	var result: Dictionary = SizeChangeRules.evaluate(GameState.heart_spring_chapter, is_at_fairy_ring(),
		data.glow, CONFIG)
	if not bool(result["allowed"]):
		_refuse(str(result["reason"]))
		return false
	if is_fairy and not has_room_for_human():
		_refuse("hint.transform.no_room")
		return false
	var cost: float = float(result["cost"])
	if cost > 0.0:
		data.glow = maxf(0.0, data.glow - cost)
		EventBus.glow_changed.emit(data.player_id, data.glow, data.max_glow)
	_transform_to_fairy = not is_fairy
	_transform_swapped = false
	flying = false
	_fly_height = 0.0
	_trail.emitting = false
	_burst.restart()
	_burst.emitting = true
	AudioManager.play_sfx(SFX_TO_FAIRY if _transform_to_fairy else SFX_TO_HUMAN, 0.0, 0.0)
	camera_punch_requested.emit(Vector2.UP if _transform_to_fairy else Vector2.DOWN)
	state.transition(&"transforming")
	return true


func is_at_fairy_ring() -> bool:
	for ring: Node in get_tree().get_nodes_in_group(&"fairy_rings"):
		var d: Vector2 = global_position - (ring as Node2D).global_position
		if (d.x / FAIRY_RING_RADII.x) ** 2 + (d.y / FAIRY_RING_RADII.y) ** 2 <= 1.0:
			return true
	return false


## Passt Klio in Menschengröße an diese Stelle (keine Wand, kein Zaun)?
func has_room_for_human(at: Vector2 = global_position) -> bool:
	var shape: RectangleShape2D = RectangleShape2D.new()
	shape.size = HUMAN_SHAPE_SIZE
	var query: PhysicsShapeQueryParameters2D = PhysicsShapeQueryParameters2D.new()
	query.shape = shape
	query.transform = Transform2D(0.0, at + _collision.position)
	query.collision_mask = PhysicsLayers.GROUND_MASK
	query.exclude = [get_rid()]
	return get_world_2d().direct_space_state.intersect_shape(query, 1).is_empty()


func call_dog() -> void:
	var dogs: Array[Node] = get_tree().get_nodes_in_group(&"soul_dog")
	AudioManager.play_sfx(SFX_CALL_DOG)
	for dog: Node in dogs:
		if dog.has_method(&"call_to"):
			dog.call(&"call_to", self)


func whistle_horse() -> void:
	AudioManager.play_sfx(SFX_WHISTLE)
	var best: Node2D = null
	for horse: Node in get_tree().get_nodes_in_group(&"horses"):
		var h: Node2D = horse as Node2D
		if best == null or h.global_position.distance_to(global_position) < best.global_position.distance_to(global_position):
			best = h
	if best != null and best.has_method(&"whistle_to"):
		best.call(&"whistle_to", self)


## Aufsitzen (von Pferd/Hund aufgerufen, nachdem sie zugestimmt haben).
func start_riding(animal: Node2D, kind: StringName) -> void:
	mount = animal
	velocity = Vector2.ZERO
	flying = false
	_fly_height = 0.0
	_trail.emitting = false
	_collision.set_deferred(&"disabled", true)
	collision_mask = 0
	_shadow.visible = false
	AudioManager.play_sfx(SFX_MOUNT)
	state.transition(&"ride_horse" if kind == &"horse" else &"ride_dog")
	flight_energy_changed.emit(flight.ratio(), false)


func try_dismount() -> bool:
	if mount == null:
		return false
	if mount.has_method(&"can_dismount") and not bool(mount.call(&"can_dismount")):
		toast_requested.emit("hint.ride.stop_first")
		return false
	var spot: Vector2 = _find_dismount_spot()
	if spot == Vector2.INF:
		_refuse("hint.ride.no_room")
		return false
	var old: Node2D = mount
	mount = null
	ride_input = Vector2.ZERO
	global_position = spot
	reset_physics_interpolation()
	_visual.position = Vector2.ZERO
	_collision.set_deferred(&"disabled", false)
	_shadow.visible = true
	if old.has_method(&"clear_rider"):
		old.call(&"clear_rider")
	AudioManager.play_sfx(SFX_MOUNT, 0.0, 0.05, &"SFX", 1.15)
	state.transition(&"fairy" if is_fairy else &"human")
	return true


## Vom Reittier jeden Physik-Frame aufgerufen, nachdem es sich bewegt hat.
## `seat` = Sitzpunkt relativ zum Tier, `behind` = hinter dem Tier zeichnen.
func sync_to_mount(animal_pos: Vector2, seat: Vector2, ride_view: String, flip: bool, behind: bool,
		speed_ratio: float) -> void:
	var sort_offset: float = -1.0 if behind else 1.0
	global_position = animal_pos + Vector2(0, sort_offset)
	_visual.position = seat - Vector2(0, sort_offset)
	view = ride_view
	facing = Vector2.LEFT if (ride_view == "side" and not flip) else (Vector2.RIGHT if ride_view == "side" else (Vector2.UP if ride_view == "up" else Vector2.DOWN))
	if is_fairy:
		_play_fairy_view()
		_fairy_body.flip_h = flip
		_wings.flip_h = flip
	else:
		_play_body("ride_" + ride_view)
		_body.flip_h = flip
		_tail.flip_h = flip
		_order_tail()
	_hair_target_override = speed_ratio * 2.0 if ride_view == "side" else 0.0


# --- Hilfen -----------------------------------------------------------------


func _move_input() -> Vector2:
	if not input_enabled:
		return Vector2.ZERO
	return Input.get_vector(&"move_left", &"move_right", &"move_up", &"move_down")


func _accelerate(target: Vector2, accel: float, friction: float, delta: float) -> void:
	var rate: float = accel if target.length() > 0.01 else friction
	velocity = velocity.move_toward(target, rate * delta)


func _update_facing(input: Vector2) -> void:
	if input.length() < 0.2:
		return
	facing = input
	var new_view: String
	if absf(input.x) > absf(input.y) * 1.1:
		new_view = "side"
	else:
		new_view = "down" if input.y > 0.0 else "up"
	var flip: bool = input.x > 0.0 if new_view == "side" else _body.flip_h
	if new_view != view or flip != _body.flip_h:
		view = new_view
		_body.flip_h = flip
		_tail.flip_h = flip
		_fairy_body.flip_h = flip
		_wings.flip_h = flip
		_order_tail()
		if is_fairy:
			_play_fairy_view()


func _order_tail() -> void:
	# Von vorn und seitlich fällt das lange Haar hinter den Körper, von hinten
	# liegt es über dem Rücken (davor).
	_human.move_child(_tail, _human.get_child_count() - 1 if view == "up" else 0)


func _play_body(anim: String) -> void:
	var anim_name: StringName = StringName(anim)
	if _body_anim.current == anim_name:
		return
	if _body_anim.current.begins_with("walk") and anim.begins_with("walk"):
		_body_anim.play_keep_phase(anim_name)
	else:
		_body_anim.play(anim_name)
	_tail_anim.play(StringName("tail_" + view))


func _play_fairy_view() -> void:
	_fairy_anim.play(StringName("fairy_" + view))
	_wings_anim.play_keep_phase(StringName("wings_" + ("side" if view == "side" else "down")))
	# Von hinten sind die Flügel vor dem Körper zu sehen
	_fairy.move_child(_wings, _fairy.get_child_count() - 1 if view == "up" else 0)


func _apply_size_visuals() -> void:
	_human.visible = not is_fairy
	_fairy.visible = is_fairy
	var rect: RectangleShape2D = RectangleShape2D.new()
	rect.size = FAIRY_SHAPE_SIZE if is_fairy else HUMAN_SHAPE_SIZE
	_collision.shape = rect
	_collision.position = Vector2(0, -rect.size.y * 0.5)
	_shadow.texture = _shadow_fairy if is_fairy else _shadow_human
	if is_fairy:
		_play_fairy_view()
	else:
		_play_body("idle_" + view)


func _update_hair(delta: float) -> void:
	var target: float
	if state.is_in(&"ride_horse"):
		target = _hair_target_override
	elif view == "side":
		target = clampf(velocity.length() / CONFIG.human_speed, 0.0, 1.0) * 2.0
	else:
		target = clampf(-velocity.x / CONFIG.human_speed, -1.0, 1.0) * 1.5
	# Gedämpfte Feder: die Haare schwingen nach, wenn Klio stoppt oder dreht
	_hair_vel += ((target - _hair_pos) * HAIR_STIFFNESS - _hair_vel * HAIR_DAMPING) * delta
	_hair_pos = clampf(_hair_pos + _hair_vel * delta, -2.4, 2.4)
	var sway_frame: int = clampi(roundi(_hair_pos), -2, 2) + 2
	_tail_anim.set_frame(sway_frame)
	_tail.offset.y = _body.offset.y + _body_anim.frame_value("bob")


func _update_visual_offsets(delta: float) -> void:
	if mount != null:
		return
	var y: float = 0.0
	if is_fairy or (state.is_in(&"transforming") and _transform_swapped and _transform_to_fairy):
		y = -roundf(sin(_time * TAU * CONFIG.hover_frequency * 0.5) * CONFIG.hover_amplitude + CONFIG.hover_amplitude) \
			- roundf(_fly_height) - 3.0
	var x: float = 0.0
	if _wobble > 0.0:
		_wobble -= delta
		x = 1.0 if int(_wobble * 30.0) % 2 == 0 else -1.0
	_visual.position = Vector2(x, y)
	_shadow.modulate.a = 0.32 - _fly_height * 0.012


func _update_focus() -> void:
	var best: Interactable = null
	var best_d: float = INF
	if state.is_in(&"human") or state.is_in(&"fairy"):
		for area: Area2D in _sensor.get_overlapping_areas():
			var it: Interactable = area as Interactable
			if it == null or not it.enabled:
				continue
			var p: Dictionary = it.prompts_for(self)
			if str(p.get("primary", "")) == "" and str(p.get("secondary", "")) == "":
				continue
			var d: float = it.global_position.distance_to(global_position) - it.focus_priority * 8.0
			if d < best_d:
				best_d = d
				best = it
	focus = best
	var prim: String = ""
	var sec: String = ""
	if focus != null:
		var p2: Dictionary = focus.prompts_for(self)
		prim = str(p2.get("primary", ""))
		sec = str(p2.get("secondary", ""))
	elif state.is_in(&"ride_horse") or state.is_in(&"ride_dog"):
		prim = "prompt.dismount"
		sec = "prompt.ride.faster" if state.is_in(&"ride_horse") else ""
	if prim != _last_prompt[0] or sec != _last_prompt[1]:
		_last_prompt = [prim, sec]
		prompt_changed.emit(prim, sec)


func _secondary_prompt() -> String:
	if focus == null:
		return ""
	return str(focus.prompts_for(self).get("secondary", ""))


func _over_low_obstacle() -> bool:
	var shape: RectangleShape2D = RectangleShape2D.new()
	shape.size = FAIRY_SHAPE_SIZE
	var query: PhysicsShapeQueryParameters2D = PhysicsShapeQueryParameters2D.new()
	query.shape = shape
	query.transform = Transform2D(0.0, global_position + _collision.position)
	query.collision_mask = PhysicsLayers.SOLID_LOW
	query.exclude = [get_rid()]
	return not get_world_2d().direct_space_state.intersect_shape(query, 1).is_empty()


func _find_dismount_spot() -> Vector2:
	var side: Vector2 = Vector2(22, 4)
	for off: Vector2 in [Vector2(side.x, side.y), Vector2(-side.x, side.y), Vector2(0, 18), Vector2(0, -14)]:
		var p: Vector2 = global_position + off
		if is_fairy or has_room_for_human(p):
			return p
	return Vector2.INF


func _refuse(reason_key: String) -> void:
	_wobble = WOBBLE_TIME
	AudioManager.play_sfx(SFX_BLOCKED)
	toast_requested.emit(reason_key)


func _on_body_frame(frame_index: int) -> void:
	if _body_anim.current.begins_with("walk") and (frame_index == 0 or frame_index == 4):
		_step_index = (_step_index + 1) % SFX_STEPS.size()
		AudioManager.play_sfx(SFX_STEPS[_step_index], -2.0, 0.08)


func _on_wing_frame(frame_index: int) -> void:
	if flying and frame_index == 0:
		AudioManager.play_sfx(SFX_WING, -4.0, 0.1)
