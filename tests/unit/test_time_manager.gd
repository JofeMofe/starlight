extends GdUnitTestSuite
## Kalender, Uhr und Mondphasen (§4.4).

func before_test() -> void:
	TimeManager.start_new_game()


func after_test() -> void:
	TimeManager.running = false
	TimeManager.release_pause(&"menu")
	TimeManager.release_pause(&"dialogue")
	TimeManager.start_new_game()


func test_new_game_starts_spring_day_one_at_six() -> void:
	assert_int(TimeManager.day).is_equal(1)
	assert_int(TimeManager.season).is_equal(0)
	assert_int(TimeManager.year).is_equal(1)
	assert_str(TimeManager.clock_text()).is_equal("06:00")


func test_config_gives_fourteen_minute_day() -> void:
	var cfg: TimeConfig = TimeManager.config
	var real_seconds: float = (cfg.day_end_minute - cfg.day_start_minute) * cfg.real_seconds_per_game_minute
	assert_float(real_seconds).is_equal_approx(14.0 * 60.0, 0.5)


func test_advance_minutes_updates_clock() -> void:
	TimeManager.advance_minutes(95.0)
	assert_str(TimeManager.clock_text()).is_equal("07:35")


func test_clock_wraps_after_midnight() -> void:
	TimeManager.minute_of_day = 24.0 * 60.0 + 30.0
	assert_str(TimeManager.clock_text()).is_equal("00:30")


func test_passing_two_am_starts_next_day_later_without_penalty() -> void:
	TimeManager.advance_minutes(float(TimeManager.config.day_end_minute))
	assert_int(TimeManager.day).is_equal(2)
	assert_bool(TimeManager.woke_from_passout).is_true()
	assert_int(int(TimeManager.minute_of_day)).is_equal(TimeManager.config.passout_wake_minute)


func test_sleep_starts_next_day_at_day_start() -> void:
	TimeManager.advance_minutes(600.0)
	TimeManager.sleep()
	assert_int(TimeManager.day).is_equal(2)
	assert_bool(TimeManager.woke_from_passout).is_false()
	assert_str(TimeManager.clock_text()).is_equal("06:00")


func test_season_and_year_rollover() -> void:
	for i: int in 28:
		TimeManager.sleep()
	assert_int(TimeManager.day).is_equal(1)
	assert_int(TimeManager.season).is_equal(1)
	for i: int in 28 * 3:
		TimeManager.sleep()
	assert_int(TimeManager.season).is_equal(0)
	assert_int(TimeManager.year).is_equal(2)
	assert_int(TimeManager.absolute_day()).is_equal(113)


func test_weekday_cycles_every_seven_days() -> void:
	assert_int(TimeManager.weekday()).is_equal(0)
	for i: int in 7:
		TimeManager.sleep()
	assert_int(TimeManager.weekday()).is_equal(0)
	TimeManager.sleep()
	assert_int(TimeManager.weekday()).is_equal(1)


func test_moon_phases_follow_season_cycle() -> void:
	assert_int(TimeManager.moon_phase_for_day(1)).is_equal(0)   # Neumond
	assert_int(TimeManager.moon_phase_for_day(2)).is_equal(1)
	assert_int(TimeManager.moon_phase_for_day(8)).is_equal(2)   # erstes Viertel
	assert_int(TimeManager.moon_phase_for_day(15)).is_equal(4)  # Vollmond
	assert_int(TimeManager.moon_phase_for_day(22)).is_equal(6)  # letztes Viertel
	assert_int(TimeManager.moon_phase_for_day(28)).is_equal(7)


func test_exactly_one_full_moon_night_per_season() -> void:
	var full_moons: int = 0
	for d: int in range(1, 29):
		if TimeManager.moon_phase_for_day(d) == TimeManager.FULL_MOON_PHASE:
			full_moons += 1
	assert_int(full_moons).is_equal(1)


func test_pause_sources_stack() -> void:
	TimeManager.running = true
	TimeManager.request_pause(&"menu")
	TimeManager.request_pause(&"dialogue")
	TimeManager.release_pause(&"menu")
	assert_bool(TimeManager.is_paused()).is_true()
	TimeManager._process(10.0)
	assert_str(TimeManager.clock_text()).is_equal("06:00")
	TimeManager.release_pause(&"dialogue")
	assert_bool(TimeManager.is_paused()).is_false()
	TimeManager._process(TimeManager.config.real_seconds_per_game_minute * 10.0)
	assert_str(TimeManager.clock_text()).is_equal("06:10")


func test_day_progress_range() -> void:
	assert_float(TimeManager.day_progress()).is_equal(0.0)
	TimeManager.minute_of_day = float(TimeManager.config.day_end_minute)
	assert_float(TimeManager.day_progress()).is_equal(1.0)


func test_dict_roundtrip() -> void:
	TimeManager.advance_minutes(123.0)
	for i: int in 40:
		TimeManager.sleep()
	var d: Dictionary = TimeManager.to_dict()
	TimeManager.start_new_game()
	TimeManager.from_dict(JSON.parse_string(JSON.stringify(d)) as Dictionary)
	assert_dict(TimeManager.to_dict()).is_equal(d)
