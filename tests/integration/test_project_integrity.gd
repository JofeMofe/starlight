extends GdUnitTestSuite
## Projektweite Integritätsprüfungen (§12.2): alle Szenen instanziierbar,
## alle Ressourcen-Referenzen auflösbar, alle Übersetzungsschlüssel in DE+EN,
## Datendateien gültig.

const SCENE_DIRS: PackedStringArray = ["res://scenes"]
const DATA_DIR: String = "res://data"
const LOCALIZATION_DIR: String = "res://data/localization"
const REQUIRED_LOCALES: PackedStringArray = ["de", "en"]


static func _collect_files(dir_path: String, extensions: PackedStringArray, out: PackedStringArray) -> void:
	var dir: DirAccess = DirAccess.open(dir_path)
	if dir == null:
		return
	for sub: String in dir.get_directories():
		_collect_files(dir_path.path_join(sub), extensions, out)
	for file: String in dir.get_files():
		if file.get_extension() in extensions:
			out.append(dir_path.path_join(file))


func test_all_scenes_instantiate() -> void:
	var scenes: PackedStringArray = []
	for d: String in SCENE_DIRS:
		_collect_files(d, ["tscn"], scenes)
	assert_int(scenes.size()).is_greater(0)
	for path: String in scenes:
		var packed: PackedScene = load(path) as PackedScene
		assert_bool(packed != null).override_failure_message("Szene lädt nicht: " + path).is_true()
		if packed == null:
			continue
		var instance: Node = packed.instantiate()
		assert_bool(instance != null).override_failure_message("Szene instanziiert nicht: " + path).is_true()
		# Nur instanziieren, nicht in den Baum hängen: _ready() einer Szene
		# darf die globale Spielsituation (Szenenwechsel etc.) nicht auslösen.
		instance.free()


func test_all_resource_references_exist() -> void:
	var files: PackedStringArray = []
	_collect_files("res://scenes", ["tscn", "tres"], files)
	_collect_files(DATA_DIR, ["tres"], files)
	var regex: RegEx = RegEx.create_from_string("path=\"(res://[^\"]+)\"")
	for path: String in files:
		var text: String = FileAccess.get_file_as_string(path)
		for m: RegExMatch in regex.search_all(text):
			var ref: String = m.get_string(1)
			assert_bool(ResourceLoader.exists(ref)) \
				.override_failure_message("%s verweist auf fehlende Ressource %s" % [path, ref]) \
				.is_true()


func test_all_translation_keys_present_in_all_locales() -> void:
	var csvs: PackedStringArray = []
	_collect_files(LOCALIZATION_DIR, ["csv"], csvs)
	assert_int(csvs.size()).is_greater(0)
	for path: String in csvs:
		var file: FileAccess = FileAccess.open(path, FileAccess.READ)
		var header: PackedStringArray = file.get_csv_line()
		assert_str(header[0]).is_equal("keys")
		for locale: String in REQUIRED_LOCALES:
			assert_bool(locale in header).override_failure_message("%s: Spalte %s fehlt" % [path, locale]).is_true()
		var seen: Dictionary[String, bool] = {}
		while not file.eof_reached():
			var row: PackedStringArray = file.get_csv_line()
			if row.size() <= 1 and (row.is_empty() or row[0].is_empty()):
				continue
			var key: String = row[0]
			assert_bool(seen.has(key)).override_failure_message("%s: Schlüssel doppelt: %s" % [path, key]).is_false()
			seen[key] = true
			for locale: String in REQUIRED_LOCALES:
				var col: int = header.find(locale)
				var value: String = row[col] if col < row.size() else ""
				assert_bool(value.strip_edges().is_empty()) \
					.override_failure_message("%s: '%s' fehlt in %s" % [path, key, locale]) \
					.is_false()


func test_code_uses_only_existing_translation_keys() -> void:
	var keys: Dictionary[String, bool] = {}
	var csvs: PackedStringArray = []
	_collect_files(LOCALIZATION_DIR, ["csv"], csvs)
	for path: String in csvs:
		var file: FileAccess = FileAccess.open(path, FileAccess.READ)
		file.get_csv_line()
		while not file.eof_reached():
			var row: PackedStringArray = file.get_csv_line()
			if not row.is_empty() and not row[0].is_empty():
				keys[row[0]] = true
	var scripts: PackedStringArray = []
	_collect_files("res://scenes", ["gd"], scripts)
	_collect_files("res://scripts", ["gd"], scripts)
	var regex: RegEx = RegEx.create_from_string("(?:tr|text)\\(\"((?:ui|dlg|item|npc|sys)\\.[a-z0-9_.]+)\"")
	for path: String in scripts:
		for m: RegExMatch in regex.search_all(FileAccess.get_file_as_string(path)):
			assert_bool(keys.has(m.get_string(1))) \
				.override_failure_message("%s nutzt unbekannten Schlüssel %s" % [path, m.get_string(1)]) \
				.is_true()


func test_all_json_data_parses() -> void:
	var files: PackedStringArray = []
	_collect_files(DATA_DIR, ["json"], files)
	assert_int(files.size()).is_greater(0)
	for path: String in files:
		var json: JSON = JSON.new()
		var err: Error = json.parse(FileAccess.get_file_as_string(path))
		assert_bool(err == OK) \
			.override_failure_message("%s: %s (Zeile %d)" % [path, json.get_error_message(), json.get_error_line()]) \
			.is_true()


func test_main_scene_and_autoloads_configured() -> void:
	var main: String = str(ProjectSettings.get_setting("application/run/main_scene"))
	assert_bool(ResourceLoader.exists(main)).is_true()
	for autoload: String in ["EventBus", "GameState", "TimeManager", "WeatherManager", "SaveManager",
			"AudioManager", "SceneRouter", "DialogueManager", "InputGlyphs", "Settings", "Localization"]:
		assert_bool(ProjectSettings.has_setting("autoload/" + autoload)) \
			.override_failure_message("Autoload fehlt: " + autoload).is_true()


func test_pixel_art_project_settings() -> void:
	assert_int(int(ProjectSettings.get_setting("display/window/size/viewport_width"))).is_equal(640)
	assert_int(int(ProjectSettings.get_setting("display/window/size/viewport_height"))).is_equal(360)
	assert_str(str(ProjectSettings.get_setting("display/window/stretch/scale_mode"))).is_equal("integer")
	assert_int(int(ProjectSettings.get_setting("rendering/textures/canvas_textures/default_texture_filter"))).is_equal(0)
	assert_bool(bool(ProjectSettings.get_setting("rendering/2d/snap/snap_2d_transforms_to_pixel"))).is_true()
