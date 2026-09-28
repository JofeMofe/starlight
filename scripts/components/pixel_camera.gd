class_name PixelCamera
extends Camera2D
## Kamera mit sanftem Nachziehen, die trotzdem immer auf ganzen Pixeln steht
## (§4.1): Die Spielerin bleibt pixelfest; nur ein kleiner Vorausblick in
## Laufrichtung gleitet weich nach (exponentiell, ~0,4 s). Dadurch gibt es
## kein Subpixel-Zittern der Figur. Dazu ein 1-Pixel-"Puls" als Rückmeldung.

const LOOK_AHEAD_FACTOR: float = 0.22
const LOOK_AHEAD_MAX: float = 22.0
const LOOK_AHEAD_RATE: float = 2.6
const VERTICAL_BIAS: float = -18.0
const PUNCH_TIME: float = 0.12

var target: Node2D = null

var _look: Vector2 = Vector2.ZERO
var _last_target_pos: Vector2 = Vector2.ZERO
var _vel: Vector2 = Vector2.ZERO
var _punch_dir: Vector2 = Vector2.ZERO
var _punch_t: float = 0.0


func _ready() -> void:
	# Nach allen Figuren aktualisieren (höhere Priorität = später)
	process_physics_priority = 100
	position_smoothing_enabled = false
	make_current()


func follow(node: Node2D) -> void:
	target = node
	_last_target_pos = node.global_position
	_look = Vector2.ZERO
	global_position = (node.global_position + Vector2(0, VERTICAL_BIAS)).round()
	reset_smoothing()
	reset_physics_interpolation()


func set_bounds(rect: Rect2i) -> void:
	limit_left = rect.position.x
	limit_top = rect.position.y
	limit_right = rect.end.x
	limit_bottom = rect.end.y


## Kurzer 1-Pixel-Stoß (Verwandlung). Respektiert "Bildschirmwackeln aus".
func punch(direction: Vector2) -> void:
	if not bool(Settings.get_value("accessibility", "screen_shake")):
		return
	_punch_dir = direction.normalized()
	_punch_t = PUNCH_TIME


func _physics_process(delta: float) -> void:
	if target == null or delta <= 0.0:
		return
	var pos: Vector2 = target.global_position
	var raw_vel: Vector2 = (pos - _last_target_pos) / delta
	_last_target_pos = pos
	_vel = _vel.lerp(raw_vel, 1.0 - exp(-10.0 * delta))
	var want: Vector2 = (_vel * LOOK_AHEAD_FACTOR).limit_length(LOOK_AHEAD_MAX)
	_look = _look.lerp(want, 1.0 - exp(-LOOK_AHEAD_RATE * delta))
	var punch_offset: Vector2 = Vector2.ZERO
	if _punch_t > 0.0:
		_punch_t -= delta
		punch_offset = _punch_dir
	global_position = (pos + Vector2(0, VERTICAL_BIAS) + _look).round() + punch_offset
