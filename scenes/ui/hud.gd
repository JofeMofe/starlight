extends CanvasLayer
## Minimales HUD (§8.7): Feenglanz, Flugkraft (nur als Fee), Kontexthinweise
## mit passenden Tasten, Gangart beim Reiten, kurze Meldungen und Hilfe (F1).

const TOAST_TIME: float = 2.6
const HELP_AUTO_TIME: float = 14.0
const HELP_LINES: Array[Array] = [
	[&"move_up", "help.move"],
	[&"size_toggle", "help.size"],
	[&"fly_jump", "help.fly"],
	[&"interact", "help.interact"],
	[&"fly_jump", "help.ride"],
	[&"dog_call", "help.dog"],
	[&"whistle", "help.whistle"],
	[&"toggle_help", "help.toggle"],
	[&"debug_fps", "help.fps"],
]

var _klio: Klio = null
var _toast_t: float = 0.0
var _help_t: float = HELP_AUTO_TIME
var _prompt_keys: Array[String] = ["", ""]

@onready var _glow_bar: ProgressBar = %GlowBar
@onready var _flight: Control = %Flight
@onready var _flight_bar: ProgressBar = %FlightBar
@onready var _prompt: Label = %Prompt
@onready var _gait: Label = %Gait
@onready var _toast: Label = %Toast
@onready var _help: PanelContainer = %Help
@onready var _help_text: Label = %HelpText
@onready var _fps: Label = %Fps


func _ready() -> void:
	EventBus.glow_changed.connect(_on_glow_changed)
	EventBus.locale_changed.connect(func(_l: String) -> void: _refresh_texts())
	EventBus.input_device_changed.connect(func(_g: bool) -> void: _refresh_texts())
	var p: PlayerData = GameState.local_player()
	_on_glow_changed(p.player_id, p.glow, p.max_glow)
	_flight.visible = false
	_toast.visible = false
	_gait.text = ""
	_refresh_texts()


func bind(klio: Klio) -> void:
	_klio = klio
	klio.prompt_changed.connect(_on_prompt_changed)
	klio.toast_requested.connect(show_toast)
	klio.flight_energy_changed.connect(_on_flight)
	klio.gait_changed.connect(_on_gait)
	klio.size_changed.connect(func(_f: bool) -> void: _gait.text = "")


func show_toast(text_key: String) -> void:
	_toast.text = tr(text_key)
	_toast.visible = true
	_toast.modulate.a = 1.0
	_toast_t = TOAST_TIME


func _process(delta: float) -> void:
	if _toast_t > 0.0:
		_toast_t -= delta
		_toast.modulate.a = clampf(_toast_t / 0.5, 0.0, 1.0)
		_toast.visible = _toast_t > 0.0
	if _fps.visible:
		_fps.text = "%d FPS  %.1f ms" % [Engine.get_frames_per_second(), delta * 1000.0]
	if _help_t > 0.0:
		_help_t -= delta
		_help.modulate.a = clampf(_help_t, 0.0, 1.0)
		_help.visible = _help_t > 0.0


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"debug_fps"):
		_fps.visible = not _fps.visible
	if event.is_action_pressed(&"toggle_help"):
		var show_help: bool = not (_help.visible and _help.modulate.a > 0.5)
		_help_t = INF if show_help else 0.0
		_help.visible = show_help
		_help.modulate.a = 1.0


func _on_glow_changed(_player_id: int, value: float, max_value: float) -> void:
	_glow_bar.max_value = max_value
	_glow_bar.value = value


func _on_flight(ratio: float, visible_now: bool) -> void:
	_flight.visible = visible_now
	_flight_bar.value = ratio * 100.0


func _on_gait(gait_key: String) -> void:
	_gait.text = tr(gait_key) if gait_key != "" else ""


func _on_prompt_changed(primary: String, secondary: String) -> void:
	_prompt_keys = [primary, secondary]
	if primary == "" and _klio != null and _klio.mount == null:
		_gait.text = ""
	_refresh_prompt()


func _refresh_prompt() -> void:
	var parts: PackedStringArray = []
	if _prompt_keys[0] != "":
		parts.append("[%s] %s" % [InputGlyphs.label_for(&"interact"), tr(_prompt_keys[0])])
	if _prompt_keys[1] != "":
		parts.append("[%s] %s" % [InputGlyphs.label_for(&"fly_jump"), tr(_prompt_keys[1])])
	_prompt.text = "    ".join(parts)


func _refresh_texts() -> void:
	var lines: PackedStringArray = [tr("help.title")]
	for entry: Array in HELP_LINES:
		var action: StringName = entry[0] as StringName
		var key_text: String = tr("help.move_keys_pad") if action == &"move_up" and InputGlyphs.using_gamepad \
			else (tr("help.move_keys") if action == &"move_up" else InputGlyphs.label_for(action))
		lines.append("%s  %s" % [key_text, tr(str(entry[1]))])
	_help_text.text = "\n".join(lines)
	_refresh_prompt()
