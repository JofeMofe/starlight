extends Node
## Einstiegspunkt. Wertet Kommandozeilen-Schalter aus (über App) und wechselt
## zur Startszene. Später: Titelbildschirm statt Testszene.


func _ready() -> void:
	if App.screenshot_path != "":
		App.take_scheduled_screenshot_and_quit()
	SceneRouter.goto.call_deferred(App.start_scene, &"", false)
