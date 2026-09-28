class_name SheetAnimator
extends Node
## Spielt Animationen eines Spritesheets der Asset-Pipeline ab (PNG + JSON).
## Die JSON-Datei liefert Framegröße, Zeilen, Frame-Dauern (bewusstes Timing)
## und optionale Zusatzdaten wie "bob" (Körperversatz pro Frame).

signal frame_changed(frame_index: int)
signal finished(anim: StringName)

@export var sprite: Sprite2D
@export_file("*.json") var meta_path: String = ""
@export var autoplay: StringName = &""

var speed_scale: float = 1.0
var current: StringName = &""
var frame: int = 0
var frame_size: Vector2i = Vector2i.ZERO

var _anims: Dictionary = {}
var _elapsed_ms: float = 0.0
var _playing: bool = false


func _ready() -> void:
	if meta_path != "":
		load_meta(meta_path)
	if autoplay != &"":
		play(autoplay)


func load_meta(path: String) -> void:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if parsed is not Dictionary:
		push_error("SheetAnimator: %s ungültig" % path)
		return
	var meta: Dictionary = parsed as Dictionary
	var fs: Array = meta.get("frame_size", [0, 0]) as Array
	frame_size = Vector2i(int(fs[0]), int(fs[1]))
	_anims = meta.get("animations", {}) as Dictionary
	if sprite != null and sprite.texture != null:
		sprite.region_enabled = true
		sprite.hframes = 1
		sprite.vframes = 1


func has_anim(anim: StringName) -> bool:
	return _anims.has(String(anim))


func play(anim: StringName, restart: bool = false) -> void:
	if not has_anim(anim):
		push_error("SheetAnimator: Animation '%s' fehlt in %s" % [anim, meta_path])
		return
	if anim == current and _playing and not restart:
		return
	current = anim
	frame = 0
	_elapsed_ms = 0.0
	_playing = true
	_apply()


## Wechselt die Animation, behält aber die Phase (z. B. Richtungswechsel im Lauf).
func play_keep_phase(anim: StringName) -> void:
	if anim == current:
		return
	var keep: int = frame
	play(anim)
	frame = keep % frame_count()
	_apply()


func stop() -> void:
	_playing = false


## Setzt einen festen Frame und hält die Animation an (z. B. Haar-Schwung,
## der per Code statt per Zeit gewählt wird).
func set_frame(index: int) -> void:
	_playing = false
	frame = clampi(index, 0, frame_count() - 1)
	_apply()


func frame_count() -> int:
	return int((_anims.get(String(current), {}) as Dictionary).get("frames", 1))


## Zusatzwert des aktuellen Frames (z. B. "bob"), 0 falls nicht vorhanden.
func frame_value(key: String) -> int:
	var data: Dictionary = _anims.get(String(current), {}) as Dictionary
	var values: Array = data.get(key, []) as Array
	return int(values[frame]) if frame < values.size() else 0


func _process(delta: float) -> void:
	if not _playing or current == &"":
		return
	var data: Dictionary = _anims[String(current)] as Dictionary
	var durations: Array = data.get("durations_ms", []) as Array
	_elapsed_ms += delta * 1000.0 * speed_scale
	var dur: float = float(durations[frame]) if frame < durations.size() else 100.0
	while _elapsed_ms >= dur:
		_elapsed_ms -= dur
		if frame + 1 >= int(data.get("frames", 1)):
			if not bool(data.get("loop", true)):
				_playing = false
				finished.emit(current)
				return
			frame = 0
		else:
			frame += 1
		frame_changed.emit(frame)
		dur = float(durations[frame]) if frame < durations.size() else 100.0
	_apply()


func _apply() -> void:
	if sprite == null or current == &"":
		return
	var data: Dictionary = _anims[String(current)] as Dictionary
	var row: int = int(data.get("row", 0))
	sprite.region_rect = Rect2(frame * frame_size.x, row * frame_size.y, frame_size.x, frame_size.y)
