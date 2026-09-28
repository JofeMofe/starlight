extends GdUnitTestSuite
## Speichern/Laden: Rundreise, atomisches Schreiben mit Backup, Migration (§4.5).

const TEST_ROOT: String = "user://test_saves"

var _original_root: String


func before_test() -> void:
	_original_root = SaveManager.save_root
	SaveManager.save_root = TEST_ROOT
	GameState.reset()
	TimeManager.start_new_game()
	WeatherManager.new_world(4242)


func after_test() -> void:
	for slot: String in SaveManager.SLOTS:
		SaveManager.delete_slot(slot)
	DirAccess.remove_absolute(TEST_ROOT)
	SaveManager.save_root = _original_root
	GameState.reset()
	TimeManager.start_new_game()


func _mutate_state() -> void:
	var klio: PlayerData = GameState.local_player()
	klio.money = 1234
	klio.glow = 42.5
	klio.is_fairy = true
	klio.position = Vector2(100.5, -32.0)
	GameState.farm_name = "Sternenhof"
	GameState.soul_dog_id = &"border_collie_mix"
	GameState.heart_spring_points = 77
	GameState.set_flag(&"met_elowen")
	for i: int in 30:
		TimeManager.sleep()
	TimeManager.advance_minutes(185.0)


func test_roundtrip_restores_identical_state() -> void:
	_mutate_state()
	var state_before: Dictionary = SaveManager.collect_state()
	assert_int(SaveManager.save_game("1", false)).is_equal(OK)
	GameState.reset()
	TimeManager.start_new_game()
	WeatherManager.new_world(1)
	assert_int(SaveManager.load_game("1")).is_equal(OK)
	var state_after: Dictionary = SaveManager.collect_state()
	# Über JSON normalisieren, da gespeicherte Zahlen als float zurückkommen.
	assert_str(JSON.stringify(state_after, "", true)).is_equal(JSON.stringify(state_before, "", true))
	assert_str(GameState.local_player().character_name).is_equal("Klio")


func test_second_save_keeps_backup_of_previous() -> void:
	SaveManager.save_game("2", false)
	GameState.local_player().money = 999
	SaveManager.save_game("2", false)
	var dir: String = SaveManager.slot_dir("2")
	assert_bool(FileAccess.file_exists(dir.path_join("save.json.bak"))).is_true()
	assert_bool(FileAccess.file_exists(dir.path_join("save.json.tmp"))).is_false()
	var backup: Variant = JSON.parse_string(FileAccess.get_file_as_string(dir.path_join("save.json.bak")))
	var players: Array = ((backup as Dictionary)["game_state"] as Dictionary)["players"] as Array
	assert_int(int((players[0] as Dictionary)["money"])).is_equal(0)


func test_corrupt_save_falls_back_to_backup() -> void:
	GameState.local_player().money = 5
	SaveManager.save_game("3", false)
	GameState.local_player().money = 6
	SaveManager.save_game("3", false)
	var file: FileAccess = FileAccess.open(SaveManager.slot_dir("3").path_join("save.json"), FileAccess.WRITE)
	file.store_string("{ kaputt")
	file.close()
	assert_int(SaveManager.load_game("3")).is_equal(OK)
	assert_int(GameState.local_player().money).is_equal(5)


func test_meta_contains_display_info() -> void:
	GameState.farm_name = "Glimmerhof"
	SaveManager.save_game("1", false)
	var meta: Dictionary = SaveManager.read_meta("1")
	assert_str(str(meta["farm_name"])).is_equal("Glimmerhof")
	assert_str(str(meta["character_name"])).is_equal("Klio")
	assert_str(str(meta["season"])).is_equal("spring")


func test_migration_from_version_zero() -> void:
	var legacy: Dictionary = {"game_state": {"farm_name": "Alt"}, "time": {"day": 3}}
	var migrated: Dictionary = SaveManager.migrate(legacy)
	assert_int(int(migrated["save_version"])).is_equal(SaveManager.SAVE_VERSION)
	assert_bool(migrated.has("weather")).is_true()


func test_unknown_slot_is_rejected() -> void:
	assert_int(SaveManager.save_game("99", false)).is_equal(ERR_INVALID_PARAMETER)
