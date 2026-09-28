extends Node
## Headless-Smoke-Bot (§12.3): spielt Spieltage im Schnelldurchlauf.
##
## M0-Umfang: Szenenwechsel über SceneRouter, Uhr läuft über volle Tage,
## Schlafengehen löst Autosave aus, der Autosave wird geladen und muss den
## identischen Zustand liefern. Ab M2/M4 kommen Tierpflege, Dorfbesuch usw. hinzu.
## Ergebnis: Exit-Code 0 und "SMOKE_RUN OK", sonst Exit-Code 1.

const DAYS_TO_PLAY: int = 7
const MINUTES_PER_FRAME: float = 45.0
const BEDTIME_MINUTE: int = 22 * 60
const SMOKE_SAVE_ROOT: String = "user://smoke_saves"
const VISIT_SCENE: String = "res://scenes/main/m0_test_scene.tscn"
const TIMEOUT_FRAMES: int = 20000

var _failures: PackedStringArray = []


func _ready() -> void:
	SaveManager.save_root = SMOKE_SAVE_ROOT
	_detach_from_scene.call_deferred()


## Der Bot ist anfangs selbst die aktuelle Szene und würde beim ersten
## Szenenwechsel freigegeben. Ein Platzhalter übernimmt die Rolle der
## aktuellen Szene; der Bot bleibt als eigenständiger Knoten unter root.
func _detach_from_scene() -> void:
	var placeholder: Node = Node.new()
	placeholder.name = "SmokePlaceholder"
	get_tree().root.add_child(placeholder)
	get_tree().current_scene = placeholder
	_run()


func _run() -> void:
	GameState.reset()
	GameState.farm_name = "Smoke-Hof"
	TimeManager.start_new_game()
	WeatherManager.new_world(20260928)
	TimeManager.running = true

	var frames: int = 0
	var days_done: int = 0
	var passout_day: int = 3  # an diesem Tag bleibt der Bot bis 02:00 wach
	while days_done < DAYS_TO_PLAY and frames < TIMEOUT_FRAMES:
		var start_day: int = TimeManager.absolute_day()
		if TimeManager.day == passout_day:
			# Bis 02:00 laufen lassen -> automatisches Einschlafen (ohne Autosave-Pflicht)
			while TimeManager.absolute_day() == start_day and frames < TIMEOUT_FRAMES:
				TimeManager.advance_minutes(MINUTES_PER_FRAME)
				frames += 1
				await get_tree().process_frame
			_expect(TimeManager.woke_from_passout, "Einschlafen um 02:00 nicht erkannt")
		else:
			while TimeManager.minute_of_day < BEDTIME_MINUTE and frames < TIMEOUT_FRAMES:
				TimeManager.advance_minutes(MINUTES_PER_FRAME)
				frames += 1
				await get_tree().process_frame
			GameState.add_money(GameState.LOCAL_PLAYER_ID, 25)
			TimeManager.sleep()
			# Autosave läuft deferred; zwei Frames warten
			await get_tree().process_frame
			await get_tree().process_frame
			_check_autosave_roundtrip()
		days_done += 1
		print("[Smoke] Tag %d beendet -> jetzt Tag %d, %s, Wetter %s" % [
			days_done, TimeManager.day, TimeManager.clock_text(), WeatherManager.current])
		if days_done == 2:
			await _visit_scene()

	TimeManager.running = false
	_expect(days_done == DAYS_TO_PLAY, "nur %d von %d Tagen gespielt" % [days_done, DAYS_TO_PLAY])
	_expect(TimeManager.day == 1 + DAYS_TO_PLAY, "Kalender steht auf Tag %d" % TimeManager.day)
	for slot: String in SaveManager.SLOTS:
		SaveManager.delete_slot(slot)
	DirAccess.remove_absolute(SMOKE_SAVE_ROOT)
	if _failures.is_empty():
		print("SMOKE_RUN OK – %d Tage, %d Frames" % [days_done, frames])
		get_tree().quit(0)
	else:
		for f: String in _failures:
			printerr("SMOKE_RUN FEHLER: ", f)
		get_tree().quit(1)


func _check_autosave_roundtrip() -> void:
	_expect(SaveManager.has_save(SaveManager.AUTOSAVE_SLOT), "kein Autosave nach dem Schlafen")
	# Die Uhr läuft zwischen Autosave und Prüfung weiter, daher wird gegen den
	# Dateiinhalt verglichen: Laden -> erneut sammeln muss ihn exakt ergeben.
	TimeManager.running = false
	var saved: Dictionary = SaveManager.read_save(SaveManager.AUTOSAVE_SLOT)
	GameState.reset()
	TimeManager.start_new_game()
	var err: Error = SaveManager.load_game(SaveManager.AUTOSAVE_SLOT)
	_expect(err == OK, "Autosave nicht ladbar: %s" % error_string(err))
	var reloaded: Dictionary = JSON.parse_string(JSON.stringify(SaveManager.collect_state())) as Dictionary
	var expected: String = JSON.stringify(saved, "", true)
	var actual: String = JSON.stringify(reloaded, "", true)
	if expected != actual:
		printerr("[Smoke] erwartet: ", expected)
		printerr("[Smoke] erhalten: ", actual)
	_expect(expected == actual, "Autosave-Rundreise weicht ab")
	TimeManager.running = true


func _visit_scene() -> void:
	SceneRouter.goto(VISIT_SCENE, &"", true)
	var guard: int = 0
	while (SceneRouter.is_transitioning or get_tree().current_scene == null
			or get_tree().current_scene.scene_file_path != VISIT_SCENE) and guard < 600:
		guard += 1
		await get_tree().process_frame
	_expect(guard < 600, "Szenenwechsel nach %s hängt" % VISIT_SCENE)
	print("[Smoke] Szene besucht: ", VISIT_SCENE)


func _expect(condition: bool, message: String) -> void:
	if not condition:
		_failures.append(message)
