extends GdUnitTestSuite
## Eingabe-Bindungen, Wetter-Determinismus, Dialogbedingungen, Einstellungen.


func test_binding_strings_roundtrip() -> void:
	for binding: String in ["key:W", "key:Space", "key:F12", "mouse:left", "mouse:wheel_up",
			"joy_button:a", "joy_button:dpad_up", "joy_axis:left_y-", "joy_axis:rt+"]:
		var event: InputEvent = InputBinding.to_event(binding)
		assert_object(event).is_not_null()
		assert_str(InputBinding.from_event(event)).is_equal(binding)


func test_invalid_binding_returns_null() -> void:
	assert_object(InputBinding.to_event("key:NichtEineTaste")).is_null()
	assert_object(InputBinding.to_event("joy_axis:left_y")).is_null()
	assert_object(InputBinding.to_event("banane:1")).is_null()


func test_all_default_actions_are_registered() -> void:
	for action: StringName in [&"move_up", &"interact", &"size_toggle", &"fly_jump",
			&"inventory", &"dog_call", &"whistle", &"tool_1", &"tool_10"]:
		assert_bool(InputMap.has_action(action)).is_true()
		assert_int(InputMap.action_get_events(action).size()).is_greater(0)


func test_weather_is_deterministic_and_forecast_matches() -> void:
	WeatherManager.new_world(777)
	var first: StringName = WeatherManager.weather_for_day(10)
	for i: int in 5:
		assert_str(String(WeatherManager.weather_for_day(10))).is_equal(String(first))
	TimeManager.start_new_game()
	var fc: Array[StringName] = WeatherManager.forecast()
	assert_int(fc.size()).is_equal(3)
	assert_str(String(fc[1])).is_equal(String(WeatherManager.weather_for_day(2)))


func test_first_day_of_season_is_sunny() -> void:
	for seed_value: int in [1, 2, 3, 99]:
		WeatherManager.new_world(seed_value)
		for season_start: int in [1, 29, 57, 85]:
			assert_str(String(WeatherManager.weather_for_day(season_start))).is_equal("sunny")


func test_winter_has_snow_and_summer_none() -> void:
	WeatherManager.new_world(5)
	var summer_snow: int = 0
	var winter_snow: int = 0
	for d: int in range(29, 57):
		if WeatherManager.weather_for_day(d) == &"snow":
			summer_snow += 1
	for d: int in range(85, 113):
		if WeatherManager.weather_for_day(d) == &"snow":
			winter_snow += 1
	assert_int(summer_snow).is_equal(0)
	assert_int(winter_snow).is_greater(0)


func test_dialogue_conditions() -> void:
	var ctx: Dictionary = {"hearts": 4, "season": "spring", "dog_present": true,
		"flags": {"met_frida": true}, "hour": 10}
	assert_bool(DialogueConditions.met({}, ctx)).is_true()
	assert_bool(DialogueConditions.met({"min_hearts": 2, "season": "spring"}, ctx)).is_true()
	assert_bool(DialogueConditions.met({"min_hearts": 6}, ctx)).is_false()
	assert_bool(DialogueConditions.met({"flag": "met_frida", "dog_present": true}, ctx)).is_true()
	assert_bool(DialogueConditions.met({"not_flag": "met_frida"}, ctx)).is_false()
	assert_bool(DialogueConditions.met({"max_hour": 9}, ctx)).is_false()


func test_settings_defaults_available() -> void:
	assert_float(float(Settings.get_value("audio", "Music"))).is_between(0.0, 1.0)
	assert_str(str(Settings.get_value("general", "locale"))).is_equal("de")
	assert_bool(bool(Settings.get_value("accessibility", "relaxed_mode"))).is_false()


func test_relaxed_mode_slows_time() -> void:
	Settings.set_value("accessibility", "relaxed_mode", true)
	assert_float(TimeManager.time_scale).is_equal(TimeManager.config.relaxed_mode_factor)
	Settings.set_value("accessibility", "relaxed_mode", false)
	assert_float(TimeManager.time_scale).is_equal(1.0)


func test_localization_placeholders() -> void:
	Localization.set_locale("de")
	assert_str(Localization.text("ui.m0.hint", {"key": "F2"})).is_equal("Taste F2: Sprache wechseln")
	Localization.set_locale("en")
	assert_str(Localization.text("ui.m0.hint", {"key": "F2"})).is_equal("Key F2: switch language")
	Localization.set_locale("de")
