extends Node
## Wetter pro Tag. Deterministisch aus Welt-Seed + fortlaufendem Tag berechnet,
## daher ist die 3-Tage-Vorschau (Wetterstein/Fernseher) immer konsistent mit
## dem tatsächlichen Wetter und muss nicht gespeichert werden.

const CONFIG_PATH: String = "res://data/config/weather.json"

var world_seed: int = 0
var current: StringName = &"sunny"
var forecast_days: int = 3

var _weights: Dictionary = {}
var _first_day_weather: StringName = &"sunny"


func _init() -> void:
	_load_config()


func _ready() -> void:
	EventBus.day_started.connect(_on_day_started)


func new_world(seed_value: int) -> void:
	world_seed = seed_value
	refresh_current()


## Wetter eines fortlaufenden Tages (1 = erster Spieltag).
func weather_for_day(absolute_day: int) -> StringName:
	var days_per_season: int = TimeManager.config.days_per_season
	var seasons: int = TimeManager.config.seasons_per_year
	var day_of_season: int = ((absolute_day - 1) % days_per_season) + 1
	if day_of_season == 1:
		return _first_day_weather
	var season_index: int = ((absolute_day - 1) / days_per_season) % seasons
	var weights: Dictionary = _weights.get(String(TimeManager.SEASON_KEYS[season_index]), {}) as Dictionary
	var rng: RandomNumberGenerator = RandomNumberGenerator.new()
	rng.seed = hash([world_seed, absolute_day])
	var total: float = 0.0
	for w: Variant in weights.values():
		total += float(w)
	var roll: float = rng.randf() * total
	for key: Variant in weights:
		roll -= float(weights[key])
		if roll < 0.0:
			return StringName(str(key))
	return &"sunny"


## Wetter für heute und die nächsten `forecast_days - 1` Tage.
func forecast() -> Array[StringName]:
	var out: Array[StringName] = []
	var today: int = TimeManager.absolute_day()
	for i: int in forecast_days:
		out.append(weather_for_day(today + i))
	return out


func refresh_current() -> void:
	var w: StringName = weather_for_day(TimeManager.absolute_day())
	if w != current:
		current = w
		EventBus.weather_changed.emit(current)


func to_dict() -> Dictionary:
	return {"world_seed": world_seed}


func from_dict(d: Dictionary) -> void:
	world_seed = int(d.get("world_seed", 0))
	current = weather_for_day(TimeManager.absolute_day())


func _on_day_started(_day: int, _season: int, _year: int) -> void:
	refresh_current()


func _load_config() -> void:
	var text: String = FileAccess.get_file_as_string(CONFIG_PATH)
	var parsed: Variant = JSON.parse_string(text)
	if parsed is not Dictionary:
		push_error("WeatherManager: %s ungültig" % CONFIG_PATH)
		return
	var cfg: Dictionary = parsed as Dictionary
	_weights = cfg.get("weights", {}) as Dictionary
	forecast_days = int(cfg.get("forecast_days", 3))
	_first_day_weather = StringName(str(cfg.get("first_day_of_season", "sunny")))
