class_name HorseGait
extends RefCounted
## Gangarten-Logik beim Reiten (rein, testbar):
## Leertaste antippen = eine Gangart schneller (Schritt -> Trab -> Galopp),
## im Galopp = Sprung. Richtung loslassen = das Pferd wird sanft langsamer.

enum Gait { HALT, WALK, TROT, CANTER }

const ANIM_NAMES: Array[StringName] = [&"idle", &"walk", &"trot", &"canter"]

var gait: Gait = Gait.HALT
var speed: float = 0.0
var heading: Vector2 = Vector2.LEFT

var _config: MovementConfig


func _init(config: MovementConfig) -> void:
	_config = config


func target_speed_for(g: Gait) -> float:
	match g:
		Gait.WALK:
			return _config.horse_walk_speed
		Gait.TROT:
			return _config.horse_trot_speed
		Gait.CANTER:
			return _config.horse_canter_speed
	return 0.0


## Leertaste: schneller werden. Gibt true zurück, wenn stattdessen gesprungen
## werden soll (nur aus vollem Galopp).
func request_faster() -> bool:
	if gait == Gait.CANTER:
		return speed >= _config.horse_canter_speed * 0.8
	if gait == Gait.HALT:
		gait = Gait.WALK
	else:
		gait = (gait + 1) as Gait
	return false


## Ein Schritt der Reitphysik. `input` ist die Lenkrichtung (Länge 0..1).
func step(input: Vector2, delta: float) -> void:
	if input.length() > 0.2:
		if gait == Gait.HALT:
			gait = Gait.WALK
		var desired: Vector2 = input.normalized()
		var rate: float = deg_to_rad(_config.horse_turn_rates[clampi(gait - 1, 0, 2)])
		var angle: float = heading.angle_to(desired)
		heading = heading.rotated(clampf(angle, -rate * delta, rate * delta))
		speed = move_toward(speed, target_speed_for(gait), _accel_for(target_speed_for(gait)) * delta)
	else:
		speed = move_toward(speed, 0.0, _config.horse_decel * delta)
		# Gangart fällt passend zum Tempo zurück
		while gait > Gait.HALT and speed < target_speed_for((gait - 1) as Gait) + 1.0:
			gait = (gait - 1) as Gait
			if gait == Gait.HALT:
				break
		if speed <= 0.0:
			gait = Gait.HALT


func velocity() -> Vector2:
	return heading * speed


func anim_name() -> StringName:
	return ANIM_NAMES[gait] if speed > 1.0 else &"idle"


func _accel_for(target: float) -> float:
	return _config.horse_accel if speed < target else _config.horse_decel
