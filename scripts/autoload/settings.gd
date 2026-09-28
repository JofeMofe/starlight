extends Node
## Einstellungen in user://settings.cfg: Audio, Grafik, Barrierefreiheit,
## Sprache und Tastenbelegung. Baut beim Start die InputMap aus
## data/config/input_default.json plus gespeicherten Überschreibungen.

const SETTINGS_PATH: String = "user://settings.cfg"
const INPUT_DEFAULTS_PATH: String = "res://data/config/input_default.json"
const BUSES: Array[StringName] = [&"Master", &"Music", &"SFX", &"Ambience", &"UI", &"Voice"]

const DEFAULTS: Dictionary = {
	"audio": {
		"Master": 0.8, "Music": 0.7, "SFX": 0.8, "Ambience": 0.7, "UI": 0.7, "Voice": 0.7,
	},
	"video": {
		"fullscreen": false,
	},
	"accessibility": {
		"text_size": 0,            # 0 normal, 1 groß, 2 sehr groß
		"dyslexic_font": false,
		"colorblind_mode": "off",  # off, protanopia, deuteranopia, tritanopia
		"screen_shake": true,
		"flash_effects": true,
		"relaxed_mode": false,
		"rhythm_auto_beat": false,
		"rhythm_latency_ms": 0,
		"subtitles": false,
	},
	"general": {
		"locale": "de",
	},
}

var _config: ConfigFile = ConfigFile.new()
var _input_defaults: Dictionary = {}
var _deadzone: float = 0.25


func _ready() -> void:
	load_settings()
	_load_input_defaults()
	apply_input_map()
	apply_audio()
	apply_video()


func get_value(section: String, key: String) -> Variant:
	if _config.has_section_key(section, key):
		return _config.get_value(section, key)
	return (DEFAULTS.get(section, {}) as Dictionary).get(key)


func set_value(section: String, key: String, value: Variant) -> void:
	_config.set_value(section, key, value)
	match section:
		"audio":
			apply_audio()
		"video":
			apply_video()
	EventBus.settings_changed.emit(StringName(section))


func load_settings() -> void:
	_config = ConfigFile.new()
	if FileAccess.file_exists(SETTINGS_PATH):
		var err: Error = _config.load(SETTINGS_PATH)
		if err != OK:
			push_warning("Settings: %s nicht lesbar (%s), nutze Standardwerte" % [SETTINGS_PATH, error_string(err)])
			_config = ConfigFile.new()


func save_settings() -> Error:
	return _config.save(SETTINGS_PATH)


func apply_audio() -> void:
	for bus: StringName in BUSES:
		var idx: int = AudioServer.get_bus_index(bus)
		if idx < 0:
			push_error("Settings: Audio-Bus %s fehlt im Bus-Layout" % bus)
			continue
		var linear: float = clampf(float(get_value("audio", String(bus))), 0.0, 1.0)
		AudioServer.set_bus_volume_db(idx, linear_to_db(maxf(linear, 0.0001)))
		AudioServer.set_bus_mute(idx, linear <= 0.0001)


func apply_video() -> void:
	if DisplayServer.get_name() == "headless":
		return
	var fullscreen: bool = bool(get_value("video", "fullscreen"))
	var mode: DisplayServer.WindowMode = DisplayServer.WINDOW_MODE_FULLSCREEN if fullscreen else DisplayServer.WINDOW_MODE_WINDOWED
	if DisplayServer.window_get_mode() != mode:
		DisplayServer.window_set_mode(mode)


# --- Eingabe ---------------------------------------------------------------

func default_bindings(action: StringName) -> PackedStringArray:
	var actions: Dictionary = _input_defaults.get("actions", {}) as Dictionary
	return PackedStringArray(actions.get(String(action), []) as Array)


func bindings(action: StringName) -> PackedStringArray:
	if _config.has_section_key("input", String(action)):
		var override: Variant = _config.get_value("input", String(action))
		if override is PackedStringArray:
			return override as PackedStringArray
	return default_bindings(action)


func rebind(action: StringName, new_bindings: PackedStringArray) -> void:
	_config.set_value("input", String(action), new_bindings)
	apply_input_map()
	EventBus.settings_changed.emit(&"input")


func reset_bindings() -> void:
	if _config.has_section("input"):
		_config.erase_section("input")
	apply_input_map()
	EventBus.settings_changed.emit(&"input")


func apply_input_map() -> void:
	var actions: Dictionary = _input_defaults.get("actions", {}) as Dictionary
	for action_key: Variant in actions:
		var action: StringName = StringName(str(action_key))
		if InputMap.has_action(action):
			InputMap.action_erase_events(action)
		else:
			InputMap.add_action(action, _deadzone)
		for binding: String in bindings(action):
			var event: InputEvent = InputBinding.to_event(binding)
			if event == null:
				push_error("Settings: ungültige Bindung '%s' für %s" % [binding, action])
				continue
			InputMap.action_add_event(action, event)


func _load_input_defaults() -> void:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(INPUT_DEFAULTS_PATH))
	if parsed is not Dictionary:
		push_error("Settings: %s ungültig" % INPUT_DEFAULTS_PATH)
		return
	_input_defaults = parsed as Dictionary
	_deadzone = float(_input_defaults.get("deadzone", 0.25))
