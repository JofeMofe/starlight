extends GdUnitTestSuite
## M1-Systeme: Flugenergie, Regeln für den Größenwechsel, Gangarten des
## Pferdes, Zustandsmaschine, MapBuilder (Kantenmasken, Startpunkte).

const CONFIG: MovementConfig = preload("res://data/config/movement.tres")


func test_flight_energy_drains_and_regenerates_after_delay() -> void:
	var e: FlightEnergy = FlightEnergy.new(100.0, 50.0, 100.0, 0.5)
	assert_bool(e.use(1.0)).is_true()
	assert_float(e.value).is_equal(50.0)
	e.rest(0.3)
	assert_float(e.value).is_equal(50.0)  # noch in der Pause
	e.rest(0.3)
	assert_float(e.value).is_greater(50.0)
	e.value = 10.0
	assert_bool(e.use(1.0)).is_false()
	assert_bool(e.is_empty()).is_true()
	assert_float(e.value).is_equal(0.0)


func test_size_change_chapter_one_needs_ring() -> void:
	var r: Dictionary = SizeChangeRules.evaluate(1, false, 100.0, CONFIG)
	assert_bool(bool(r["allowed"])).is_false()
	assert_str(str(r["reason"])).is_equal(String(SizeChangeRules.REASON_NEED_RING))
	r = SizeChangeRules.evaluate(1, true, 0.0, CONFIG)
	assert_bool(bool(r["allowed"])).is_true()
	assert_float(float(r["cost"])).is_equal(0.0)


func test_size_change_chapter_two_costs_glow() -> void:
	var r: Dictionary = SizeChangeRules.evaluate(2, false, 100.0, CONFIG)
	assert_bool(bool(r["allowed"])).is_true()
	assert_float(float(r["cost"])).is_equal(CONFIG.transform_glow_cost)
	r = SizeChangeRules.evaluate(2, false, CONFIG.transform_glow_cost - 1.0, CONFIG)
	assert_bool(bool(r["allowed"])).is_false()
	assert_str(str(r["reason"])).is_equal(String(SizeChangeRules.REASON_NO_GLOW))


func test_size_change_chapter_four_is_free() -> void:
	var r: Dictionary = SizeChangeRules.evaluate(4, false, 0.0, CONFIG)
	assert_bool(bool(r["allowed"])).is_true()
	assert_float(float(r["cost"])).is_equal(0.0)


func test_horse_gait_shifts_up_and_jumps_only_from_canter() -> void:
	var g: HorseGait = HorseGait.new(CONFIG)
	assert_bool(g.request_faster()).is_false()
	assert_int(g.gait).is_equal(HorseGait.Gait.WALK)
	g.request_faster()
	g.request_faster()
	assert_int(g.gait).is_equal(HorseGait.Gait.CANTER)
	assert_bool(g.request_faster()).is_false()  # noch zu langsam zum Springen
	for i: int in 120:
		g.step(Vector2.LEFT, 1.0 / 60.0)
	assert_float(g.speed).is_equal_approx(CONFIG.horse_canter_speed, 0.5)
	assert_bool(g.request_faster()).is_true()


func test_horse_accelerates_gradually_and_stops_without_input() -> void:
	var g: HorseGait = HorseGait.new(CONFIG)
	g.request_faster()
	g.request_faster()  # Trab
	g.step(Vector2.LEFT, 0.1)
	assert_float(g.speed).is_less(CONFIG.horse_trot_speed * 0.5)
	for i: int in 300:
		g.step(Vector2.ZERO, 1.0 / 60.0)
	assert_float(g.speed).is_equal(0.0)
	assert_int(g.gait).is_equal(HorseGait.Gait.HALT)


func test_horse_turns_with_limited_rate() -> void:
	var g: HorseGait = HorseGait.new(CONFIG)
	g.heading = Vector2.LEFT
	g.gait = HorseGait.Gait.CANTER
	g.speed = CONFIG.horse_canter_speed
	g.step(Vector2.RIGHT, 0.1)
	var max_turn: float = deg_to_rad(CONFIG.horse_turn_rates[2]) * 0.1
	assert_float(absf(Vector2.LEFT.angle_to(g.heading))).is_less_equal(max_turn + 0.001)


func test_state_machine_callbacks_and_time() -> void:
	var sm: StateMachine = StateMachine.new()
	var calls: PackedStringArray = []
	sm.add(&"a", func(_d: float) -> void: calls.append("upd_a"), func() -> void: calls.append("enter_a"),
		func() -> void: calls.append("exit_a"))
	sm.add(&"b", Callable(), func() -> void: calls.append("enter_b"))
	sm.transition(&"a")
	sm.update(0.5)
	sm.update(0.25)
	assert_float(sm.time_in_state).is_equal(0.75)
	sm.transition(&"b")
	assert_array(Array(calls)).is_equal(["enter_a", "upd_a", "upd_a", "exit_a", "enter_b"])
	assert_float(sm.time_in_state).is_equal(0.0)


func test_map_builder_masks_and_spawns() -> void:
	var b: MapBuilder = MapBuilder.new("res://data/maps/test_meadow.json")
	assert_int(b.size.x).is_equal(40)
	assert_int(b.size.y).is_equal(30)
	# Kreuzung der Wege: alle vier Nachbarn sind Weg
	assert_str(b.kind_at(Vector2i(19, 16))).is_equal("path")
	assert_int(b.mask_at(Vector2i(19, 16), "path")).is_equal(MapBuilder.N | MapBuilder.E | MapBuilder.S | MapBuilder.W)
	# Zaunecke oben links: Nachbarn nur rechts und unten
	assert_int(b.mask_at(Vector2i(23, 3), "fence")).is_equal(MapBuilder.E | MapBuilder.S)
	assert_object(b.tile_set).is_not_null()
