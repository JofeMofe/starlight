extends Node
## M1-Bot: spielt die Kernmechanik auf der Test-Wiese per simulierter Eingabe
## durch und prüft die Ergebnisse. Mit `-- --shots=ORDNER` entstehen dabei
## Screenshots für die visuelle QA (nur mit Fenster, nicht headless).
## Ergebnis: "M1_BOT OK" und Exit-Code 0, sonst Liste der Fehler und Code 1.

const MEADOW: PackedScene = preload("res://scenes/world/test_meadow.tscn")
const CONFIG: MovementConfig = preload("res://data/config/movement.tres")
const WARMUP_FRAMES: int = 60

var _failures: PackedStringArray = []
var _shots_dir: String = ""
var _meadow: Node2D
var _klio: Klio
var _dog: SoulDog
var _horse: Horse
var _frame_ms: PackedFloat32Array = []


func _ready() -> void:
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("--shots="):
			_shots_dir = arg.get_slice("=", 1)
	GameState.reset()
	_meadow = MEADOW.instantiate() as Node2D
	add_child(_meadow)
	_klio = _meadow.get_node("Nav/World/Klio") as Klio
	_dog = _meadow.get_node("Nav/World/Dog") as SoulDog
	_horse = _meadow.get_node("Nav/World/Horse") as Horse
	_run.call_deferred()


func _run() -> void:
	await _frames(30)
	await _shot("01_start")
	_check(_klio.state.is_in(&"human"), "Start nicht in Menschengröße")
	_check_navigation()

	# --- Laufen: Beschleunigung und Endtempo --------------------------------
	var start: Vector2 = _klio.global_position
	await _hold(&"move_right", 0.6)
	_check(_klio.global_position.x - start.x > 30.0, "Laufen nach rechts zu kurz")
	var peak: float = _klio.velocity.length()
	_check(absf(peak - CONFIG.human_speed) < 6.0, "Endtempo %.1f statt %.1f" % [peak, CONFIG.human_speed])
	await _frames(12)
	_check(_klio.velocity.length() < 1.0, "Klio bremst nicht ab")

	# --- Verwandlung zur Fee (kostet Feenglanz abseits eines Rings) ---------
	var glow_before: float = GameState.local_player().glow
	await _tap(&"size_toggle")
	await _seconds(0.2)
	await _shot("02_transform_flash")
	await _seconds(0.4)
	_check(_klio.is_fairy, "Verwandlung zur Fee fehlgeschlagen")
	_check(is_equal_approx(GameState.local_player().glow, glow_before - CONFIG.transform_glow_cost),
		"Feenglanz nicht um %.0f gesunken" % CONFIG.transform_glow_cost)
	await _shot("03_fairy")

	# --- Hecke: zu Fuß blockiert, fliegend überquerbar ----------------------
	var above_hedge: Vector2 = Vector2(15 * 32 + 16, 19 * 32 - 14)
	_klio.global_position = above_hedge
	await _frames(3)
	await _hold(&"move_down", 0.7)
	_check(_klio.global_position.y < 19 * 32 + 20, "Fee läuft ohne Fliegen durch die Hecke (y=%.0f)" % _klio.global_position.y)
	Input.action_press(&"fly_jump")
	await _hold(&"move_down", 0.7)
	await _shot("04_flying_over_hedge")
	await _hold(&"move_down", 0.4)
	Input.action_release(&"fly_jump")
	_check(_klio.global_position.y > 19 * 32 + 20, "Fee fliegt nicht über die Hecke (y=%.0f)" % _klio.global_position.y)
	await _seconds(0.5)
	_check(not _klio.flying, "Fee landet nicht")

	# --- Kein Platz für Menschengröße -> Verwandlung wird abgelehnt ---------
	_klio.global_position = Vector2(15 * 32 + 16, 19 * 32 + 25)
	_klio.flying = true
	await _frames(3)
	var toast: Array[String] = []
	var on_toast: Callable = func(key: String) -> void: toast.append(key)
	_klio.toast_requested.connect(on_toast)
	await _tap(&"size_toggle")
	await _seconds(0.5)
	_check(_klio.is_fairy, "Verwandlung trotz fehlendem Platz")
	_check(toast.has("hint.transform.no_room"), "Kein Hinweis bei fehlendem Platz")
	_klio.toast_requested.disconnect(on_toast)

	# --- Auf dem Hund reiten (als Fee) --------------------------------------
	_klio.global_position = Vector2(20 * 32 + 16, 17 * 32 + 20)
	_dog.global_position = _klio.global_position + Vector2(10, 2)
	_dog.velocity = Vector2.ZERO
	await _frames(6)
	await _tap(&"interact")
	await _frames(4)
	_check(_klio.state.is_in(&"ride_dog"), "Fee sitzt nicht auf dem Hund")
	var dog_start: Vector2 = _dog.global_position
	await _hold(&"move_right", 1.0)
	await _shot("05_ride_dog")
	var dog_dist: float = _dog.global_position.x - dog_start.x
	_check(dog_dist > CONFIG.fairy_fly_speed * 1.0, "Hund nicht schneller als die fliegende Fee (%.0f px)" % dog_dist)
	await _frames(20)
	await _tap(&"interact")
	await _frames(4)
	_check(_klio.state.is_in(&"fairy"), "Absteigen vom Hund fehlgeschlagen")

	# --- Am Feenring kostenlos zurück in Menschengröße ----------------------
	var ring: Node2D = get_tree().get_first_node_in_group(&"fairy_rings") as Node2D
	_klio.global_position = ring.global_position
	await _frames(4)
	glow_before = GameState.local_player().glow
	await _shot("06_fairy_ring")
	await _tap(&"size_toggle")
	await _seconds(0.6)
	_check(not _klio.is_fairy, "Rückverwandlung am Feenring fehlgeschlagen")
	_check(is_equal_approx(GameState.local_player().glow, glow_before), "Feenring hat Feenglanz gekostet")

	# --- Pferd: aufsteigen, drei Gangarten, anhalten, absteigen -------------
	_klio.global_position = _horse.global_position + Vector2(24, 6)
	await _frames(6)
	await _tap(&"fly_jump")
	await _frames(4)
	_check(_klio.state.is_in(&"ride_horse"), "Aufsteigen aufs Pferd fehlgeschlagen")
	Input.action_press(&"move_left")
	await _seconds(0.8)
	_check(_horse.gait.gait == HorseGait.Gait.WALK, "Pferd nicht im Schritt")
	await _tap(&"fly_jump")
	await _seconds(0.8)
	_check(_horse.gait.gait == HorseGait.Gait.TROT, "Pferd nicht im Trab")
	await _shot("07_ride_trot")
	Input.action_release(&"move_left")
	Input.action_press(&"move_down")
	await _tap(&"fly_jump")
	await _seconds(1.2)
	_check(_horse.gait.gait == HorseGait.Gait.CANTER, "Pferd nicht im Galopp")
	await _shot("08_ride_canter_down")
	Input.action_release(&"move_down")
	Input.action_press(&"move_up")
	await _seconds(0.9)
	await _shot("09_ride_up")
	Input.action_release(&"move_up")
	await _seconds(2.0)
	_check(_horse.gait.speed < 1.0, "Pferd hält nicht an (%.0f px/s)" % _horse.gait.speed)
	await _tap(&"interact")
	await _frames(4)
	_check(_klio.state.is_in(&"human"), "Absteigen vom Pferd fehlgeschlagen")

	# --- Rufen, Pfeifen, Streicheln ------------------------------------------
	_klio.global_position = Vector2(19 * 32 + 16, 16 * 32 + 20)
	await _frames(2)
	await _tap(&"whistle")
	await _frames(2)
	_check(_horse.state.is_in(&"come") or _horse.state.is_in(&"idle"), "Pferd reagiert nicht auf den Pfiff")
	await _tap(&"dog_call")
	# Der Hund nimmt per Navigation den Weg um Zäune herum (ggf. durchs Tor)
	for i: int in 16:
		if _dog.global_position.distance_to(_klio.global_position) < 50.0:
			break
		await _seconds(0.5)
	_check(_dog.global_position.distance_to(_klio.global_position) < 50.0, "Hund kommt nicht auf Zuruf")
	await _seconds(1.5)
	_dog.global_position = _klio.global_position + Vector2(-12, 4)
	await _frames(4)
	await _tap(&"interact")
	await _frames(10)
	await _shot("10_pet_dog")
	_check(_dog.state.is_in(&"petted"), "Hund lässt sich nicht streicheln")
	await _seconds(3.0)
	await _shot("11_horse_arrived")

	_report_performance()
	# Sauber aufräumen, damit beim Beenden nichts "leakt"
	_meadow.queue_free()
	await _frames(3)
	if _failures.is_empty():
		print("M1_BOT OK")
		get_tree().quit(0)
	else:
		for f: String in _failures:
			printerr("M1_BOT FEHLER: ", f)
		get_tree().quit(1)


func _process(_delta: float) -> void:
	# CPU-Zeit pro Frame (Skripte + Physik), Ziel laut §12.5: < 8 ms
	# Die ersten Frames (Kartenaufbau, Navigationsnetz backen) zählen nicht mit
	if Engine.get_process_frames() < WARMUP_FRAMES:
		return
	var ms: float = (Performance.get_monitor(Performance.TIME_PROCESS)
		+ Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS)) * 1000.0
	_frame_ms.append(ms)


func _report_performance() -> void:
	if _frame_ms.is_empty():
		return
	var sorted: Array = Array(_frame_ms)
	sorted.sort()
	var total: float = 0.0
	for v: float in _frame_ms:
		total += v
	print("M1_BOT Frame-CPU: Mittel %.2f ms, 95%%-Perzentil %.2f ms, Max %.2f ms (%d Frames)" % [
		total / _frame_ms.size(), float(sorted[int(sorted.size() * 0.95)]), float(sorted[-1]), _frame_ms.size()])


func _check_navigation() -> void:
	var map: RID = get_viewport().world_2d.navigation_map
	NavigationServer2D.map_force_update(map)
	var path: PackedVector2Array = NavigationServer2D.map_get_path(map, _dog.global_position,
		_horse.global_position + Vector2(0, 60), true)
	_check(path.size() >= 2, "Navigationsnetz liefert keinen Weg")


func _check(condition: bool, message: String) -> void:
	if not condition:
		_failures.append(message)
		printerr("  x ", message)


func _frames(n: int) -> void:
	for i: int in n:
		await get_tree().physics_frame


func _seconds(s: float) -> void:
	await get_tree().create_timer(s, true, true).timeout


func _hold(action: StringName, s: float) -> void:
	Input.action_press(action)
	await _seconds(s)
	Input.action_release(action)


func _tap(action: StringName) -> void:
	Input.action_press(action)
	await _frames(2)
	Input.action_release(action)
	await _frames(1)


func _shot(shot_name: String) -> void:
	if _shots_dir == "" or DisplayServer.get_name() == "headless":
		return
	await RenderingServer.frame_post_draw
	App.save_screenshot("%s/%s.png" % [_shots_dir, shot_name])
