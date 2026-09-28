extends Node2D
## M0-Testszene: prüft Integer-Skalierung, Pixel-Snapping, Palette, Pixel-Font
## und Lokalisierung. Ein Funkelstern umkreist das Icon; durch Pixel-Snapping
## darf er nie zwischen zwei Pixeln "verschmieren".

const ORBIT_RADIUS: float = 34.0
const ORBIT_SPEED: float = 1.4
const BOB_AMPLITUDE: float = 2.0

@onready var _icon: Sprite2D = %Icon
@onready var _sparkle: Sprite2D = %Sparkle
@onready var _title: Label = %Title
@onready var _subtitle: Label = %Subtitle
@onready var _charset: Label = %Charset
@onready var _info: Label = %Info
@onready var _hint: Label = %Hint

var _t: float = 0.0


func _ready() -> void:
	EventBus.locale_changed.connect(_on_locale_changed)
	get_window().size_changed.connect(_refresh_texts)
	_refresh_texts()


func _process(delta: float) -> void:
	_t += delta
	_sparkle.position = _icon.position + Vector2(cos(_t * ORBIT_SPEED), sin(_t * ORBIT_SPEED)) * ORBIT_RADIUS
	_icon.position.y = 150.0 + roundf(sin(_t * 2.0) * BOB_AMPLITUDE)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"debug_toggle_locale"):
		Localization.set_locale("en" if Localization.current_locale() == "de" else "de")
	elif event.is_action_pressed(&"debug_screenshot"):
		App.save_screenshot("user://screenshots/m0_%d.png" % Time.get_ticks_msec())


func _refresh_texts() -> void:
	var win: Vector2i = get_window().size
	_title.text = tr("ui.title")
	_subtitle.text = tr("ui.m0.subtitle")
	_charset.text = tr("ui.m0.charset")
	_info.text = Localization.text("ui.m0.scale", {
		"w": win.x, "h": win.y, "s": App.pixel_scale(), "version": App.version(),
	})
	_hint.text = Localization.text("ui.m0.hint", {"key": InputGlyphs.label_for(&"debug_toggle_locale")})


func _on_locale_changed(_locale: String) -> void:
	_refresh_texts()
