extends Node
## Speichern/Laden als JSON (§4.5).
##
## Layout: <save_root>/slot_<id>/save.json (+ save.json.bak, meta.json, thumbnail.png)
## Slots: "1", "2", "3" und "autosave". Geschrieben wird atomar: erst in eine
## temporäre Datei, dann die alte Version zum Backup umbenennen, dann die neue
## an ihren Platz. Ältere Spielstände werden beim Laden schrittweise migriert.

const SAVE_VERSION: int = 1
const SLOTS: Array[String] = ["1", "2", "3", "autosave"]
const AUTOSAVE_SLOT: String = "autosave"
const SAVE_FILE: String = "save.json"
const META_FILE: String = "meta.json"
const THUMB_FILE: String = "thumbnail.png"
const THUMB_SIZE: Vector2i = Vector2i(160, 90)

## Basisordner; Tests setzen einen eigenen, um echte Spielstände nicht zu berühren.
var save_root: String = "user://saves"


func _ready() -> void:
	EventBus.day_ended.connect(_on_day_ended)


func slot_dir(slot: String) -> String:
	return "%s/slot_%s" % [save_root, slot]


func has_save(slot: String) -> bool:
	return FileAccess.file_exists(slot_dir(slot).path_join(SAVE_FILE))


## Sammelt den gesamten Spielzustand in ein Dictionary.
func collect_state() -> Dictionary:
	return {
		"save_version": SAVE_VERSION,
		"game_state": GameState.to_dict(),
		"time": TimeManager.to_dict(),
		"weather": WeatherManager.to_dict(),
	}


func apply_state(data: Dictionary) -> void:
	GameState.from_dict(data.get("game_state", {}) as Dictionary)
	TimeManager.from_dict(data.get("time", {}) as Dictionary)
	WeatherManager.from_dict(data.get("weather", {}) as Dictionary)


func save_game(slot: String, with_thumbnail: bool = true) -> Error:
	if slot not in SLOTS:
		push_error("SaveManager: unbekannter Slot '%s'" % slot)
		return ERR_INVALID_PARAMETER
	var dir: String = slot_dir(slot)
	var err: Error = DirAccess.make_dir_recursive_absolute(dir)
	if err != OK:
		return err
	err = _write_atomic(dir.path_join(SAVE_FILE), JSON.stringify(collect_state(), "\t"))
	if err != OK:
		return err
	err = _write_atomic(dir.path_join(META_FILE), JSON.stringify(_meta(), "\t"))
	if err != OK:
		return err
	if with_thumbnail and DisplayServer.get_name() != "headless":
		_save_thumbnail(dir.path_join(THUMB_FILE))
	EventBus.game_saved.emit(slot)
	return OK


func load_game(slot: String) -> Error:
	var data: Dictionary = read_save(slot)
	if data.is_empty():
		return ERR_FILE_CORRUPT
	apply_state(data)
	EventBus.game_loaded.emit(slot)
	return OK


## Liest und migriert einen Spielstand. Fällt auf das Backup zurück, falls
## die Hauptdatei fehlt oder beschädigt ist. Leeres Dictionary bei Fehlschlag.
func read_save(slot: String) -> Dictionary:
	var path: String = slot_dir(slot).path_join(SAVE_FILE)
	for candidate: String in [path, path + ".bak"]:
		var data: Dictionary = _read_json(candidate)
		if not data.is_empty():
			return migrate(data)
	return {}


func read_meta(slot: String) -> Dictionary:
	return _read_json(slot_dir(slot).path_join(META_FILE))


## Hebt einen Spielstand Version für Version auf SAVE_VERSION an.
## Neue Migration: `_migrate_<n>_to_<n+1>(data)` anlegen und SAVE_VERSION erhöhen.
func migrate(data: Dictionary) -> Dictionary:
	var version: int = int(data.get("save_version", 0))
	while version < SAVE_VERSION:
		var method: String = "_migrate_%d_to_%d" % [version, version + 1]
		if not has_method(method):
			push_error("SaveManager: Migration %s fehlt" % method)
			return {}
		data = call(method, data) as Dictionary
		version += 1
		data["save_version"] = version
	if version > SAVE_VERSION:
		push_warning("SaveManager: Spielstand-Version %d ist neuer als das Spiel (%d)" % [version, SAVE_VERSION])
	return data


func delete_slot(slot: String) -> void:
	var dir: String = slot_dir(slot)
	for file: String in [SAVE_FILE, SAVE_FILE + ".bak", META_FILE, THUMB_FILE, SAVE_FILE + ".tmp"]:
		if FileAccess.file_exists(dir.path_join(file)):
			DirAccess.remove_absolute(dir.path_join(file))
	DirAccess.remove_absolute(dir)


# --- Migrationen -----------------------------------------------------------

## Version 0 = Prototyp-Spielstände ohne Versionsfeld und ohne Wetterblock.
func _migrate_0_to_1(data: Dictionary) -> Dictionary:
	if not data.has("weather"):
		data["weather"] = {"world_seed": 0}
	return data


# --- Intern ----------------------------------------------------------------

func _meta() -> Dictionary:
	return {
		"save_version": SAVE_VERSION,
		"character_name": GameState.local_player().character_name,
		"farm_name": GameState.farm_name,
		"day": TimeManager.day,
		"season": String(TimeManager.season_key()),
		"year": TimeManager.year,
		"play_time_seconds": int(GameState.play_time_seconds),
		"saved_at_unix": int(Time.get_unix_time_from_system()),
		"game_version": str(ProjectSettings.get_setting("application/config/version", "")),
	}


func _write_atomic(path: String, content: String) -> Error:
	var tmp_path: String = path + ".tmp"
	var file: FileAccess = FileAccess.open(tmp_path, FileAccess.WRITE)
	if file == null:
		return FileAccess.get_open_error()
	file.store_string(content)
	file.flush()
	file.close()
	if FileAccess.file_exists(path):
		var bak_path: String = path + ".bak"
		if FileAccess.file_exists(bak_path):
			DirAccess.remove_absolute(bak_path)
		var err_bak: Error = DirAccess.rename_absolute(path, bak_path)
		if err_bak != OK:
			return err_bak
	return DirAccess.rename_absolute(tmp_path, path)


func _read_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	return parsed as Dictionary if parsed is Dictionary else {}


func _save_thumbnail(path: String) -> void:
	var img: Image = get_viewport().get_texture().get_image()
	img.resize(THUMB_SIZE.x, THUMB_SIZE.y, Image.INTERPOLATE_NEAREST)
	img.save_png(path)


func _on_day_ended(_day: int, _season: int, _year: int) -> void:
	# Autosave beim Schlafengehen; im Hauptmenü (keine laufende Uhr) nicht.
	if TimeManager.running:
		call_deferred(&"save_game", AUTOSAVE_SLOT)
