extends Node
## Laufzeit-Infos und Kommandozeilen-Schalter.
##
## Schalter (nach `--` bzw. direkt an die Exe angehängt):
##   --smoke                 Läuft `smoke_seconds` lang und beendet sich mit Code 0
##   --smoke-seconds=N       Dauer des Smoke-Laufs (Standard 60)
##   --scene=res://...       Startszene überschreiben (Debug, Screenshots)
##   --screenshot=user://x.png  Nach `screenshot_delay` Frames Screenshot, dann Ende
##   --screenshot-delay=N    Frames bis zum Screenshot (Standard 30)

const DEFAULT_SMOKE_SECONDS: float = 60.0
const DEFAULT_SCREENSHOT_DELAY: int = 30
const INITIAL_SCENE: String = "res://scenes/main/m0_test_scene.tscn"

var smoke_mode: bool = false
var smoke_seconds: float = DEFAULT_SMOKE_SECONDS
var start_scene: String = INITIAL_SCENE
var screenshot_path: String = ""
var screenshot_delay: int = DEFAULT_SCREENSHOT_DELAY


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_parse_args(OS.get_cmdline_args() + OS.get_cmdline_user_args())
	if smoke_mode:
		print("[App] Smoke-Modus: %.1f s" % smoke_seconds)
		get_tree().create_timer(smoke_seconds, true, false, true).timeout.connect(_finish_smoke)


func version() -> String:
	return str(ProjectSettings.get_setting("application/config/version", "0.0.0"))


func is_headless() -> bool:
	return DisplayServer.get_name() == "headless"


## Aktuelle Integer-Skalierung (1 in Headless-Läufen).
func pixel_scale() -> int:
	var base: Vector2i = Vector2i(
		int(ProjectSettings.get_setting("display/window/size/viewport_width")),
		int(ProjectSettings.get_setting("display/window/size/viewport_height")))
	var win: Vector2i = get_window().size
	return maxi(1, mini(floori(float(win.x) / base.x), floori(float(win.y) / base.y)))


## Speichert das aktuelle Bild als PNG. Der Viewport rendert in 640x360;
## das Bild wird per Nearest um die aktuelle Integer-Skalierung vergrößert,
## entspricht also Pixel für Pixel dem, was im Fenster zu sehen ist.
func save_screenshot(path: String, scale: int = 0) -> Error:
	var img: Image = get_viewport().get_texture().get_image()
	var factor: int = scale if scale > 0 else pixel_scale()
	if factor > 1:
		img.resize(img.get_width() * factor, img.get_height() * factor, Image.INTERPOLATE_NEAREST)
	var abs_path: String = ProjectSettings.globalize_path(path)
	DirAccess.make_dir_recursive_absolute(abs_path.get_base_dir())
	var err: Error = img.save_png(abs_path)
	print("[App] Screenshot %s -> %s (%dx%d)" % [error_string(err), abs_path, img.get_width(), img.get_height()])
	return err


func take_scheduled_screenshot_and_quit() -> void:
	for i: int in screenshot_delay:
		await get_tree().process_frame
	await RenderingServer.frame_post_draw
	var err: Error = save_screenshot(screenshot_path)
	get_tree().quit(0 if err == OK else 1)


func _parse_args(args: PackedStringArray) -> void:
	for arg: String in args:
		if arg == "--smoke":
			smoke_mode = true
		elif arg.begins_with("--smoke-seconds="):
			smoke_seconds = maxf(0.1, arg.get_slice("=", 1).to_float())
		elif arg.begins_with("--scene="):
			start_scene = arg.get_slice("=", 1)
		elif arg.begins_with("--screenshot="):
			screenshot_path = arg.get_slice("=", 1)
		elif arg.begins_with("--screenshot-delay="):
			screenshot_delay = maxi(1, arg.get_slice("=", 1).to_int())


func _finish_smoke() -> void:
	print("[App] SMOKE OK – %d Frames, %.1f s" % [Engine.get_process_frames(), smoke_seconds])
	get_tree().quit(0)
