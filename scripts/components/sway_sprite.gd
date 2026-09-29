class_name SwaySprite
extends Sprite2D
## Spielt die Frames eines horizontalen Streifens als ruhige Wind-Schleife ab
## (Sunnyside-Bäume). Jede Instanz startet an einer anderen Stelle, damit sich
## nebeneinanderstehende Bäume nicht im Gleichtakt wiegen.

@export var frame_time: float = 0.28

var _t: float = 0.0


func _ready() -> void:
	_t = float(absi(hash(global_position)) % 1000) / 1000.0 * frame_time * hframes
	frame = int(_t / frame_time) % hframes


func _process(delta: float) -> void:
	_t += delta
	var f: int = int(_t / frame_time) % hframes
	if f != frame:
		frame = f
