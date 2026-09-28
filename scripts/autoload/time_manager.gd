extends Node
## Uhrzeit, Tag, Jahreszeit, Jahr, Wochentag und Mondphase.
##
## Die Uhr läuft nur, wenn eine Spielszene `running = true` setzt, und steht,
## solange mindestens eine Pausenquelle aktiv ist (Menü, Dialog, Minispiel,
## Innenraum im Entspannten Modus). Zeitangaben sind Minuten seit Mitternacht
## des aktuellen Tages; nach 24:00 laufen sie weiter bis `day_end_minute` (02:00 = 1560).

enum Season { SPRING, SUMMER, AUTUMN, WINTER }

const CONFIG_PATH: String = "res://data/config/time.tres"
const SEASON_KEYS: Array[StringName] = [&"spring", &"summer", &"autumn", &"winter"]
const MOON_PHASE_KEYS: Array[StringName] = [
	&"new_moon", &"waxing_crescent", &"first_quarter", &"waxing_gibbous",
	&"full_moon", &"waning_gibbous", &"last_quarter", &"waning_crescent",
]
const FULL_MOON_PHASE: int = 4
const MINUTES_PER_HOUR: int = 60
const MINUTES_PER_DAY: int = 1440

var config: TimeConfig
var minute_of_day: float = 360.0
var day: int = 1
var season: int = Season.SPRING
var year: int = 1
## Nur wenn true, schreitet die Uhr in _process fort (Spielszenen schalten das ein).
var running: bool = false
## Zusätzlicher Faktor (z. B. Entspannter Modus), 1.0 = normal.
var time_scale: float = 1.0
## true, wenn der aktuelle Tag nach Einschlafen um 02:00 begann.
var woke_from_passout: bool = false

var _pause_sources: Dictionary[StringName, bool] = {}


func _init() -> void:
	config = load(CONFIG_PATH) as TimeConfig
	minute_of_day = float(config.day_start_minute)


func _ready() -> void:
	EventBus.settings_changed.connect(_on_settings_changed)
	_apply_relaxed_mode()


func _process(delta: float) -> void:
	if running and not is_paused():
		advance_minutes(delta * time_scale / config.real_seconds_per_game_minute)


# --- Steuerung -------------------------------------------------------------

func start_new_game() -> void:
	day = 1
	season = Season.SPRING
	year = 1
	minute_of_day = float(config.day_start_minute)
	woke_from_passout = false
	EventBus.day_started.emit(day, season, year)


## Lässt die Uhr um `minutes` Spielminuten fortschreiten und sendet für jede
## überschrittene volle Minute/Stunde die Signale. Erreicht die Uhr 02:00,
## schläft Klio automatisch ein.
func advance_minutes(minutes: float) -> void:
	if minutes <= 0.0:
		return
	var before: int = int(minute_of_day)
	minute_of_day = minf(minute_of_day + minutes, float(config.day_end_minute))
	var after: int = int(minute_of_day)
	for m: int in range(before + 1, after + 1):
		EventBus.minute_changed.emit(m)
		if m % MINUTES_PER_HOUR == 0:
			@warning_ignore("integer_division")
			EventBus.hour_changed.emit((m / MINUTES_PER_HOUR) % 24)
	if after >= config.day_end_minute:
		pass_out()


## Regulär schlafen gehen: nächster Tag beginnt um day_start_minute.
func sleep() -> void:
	_begin_next_day(config.day_start_minute, false)


## Automatisches Einschlafen um 02:00 – keine Strafe, nur späteres Aufwachen.
func pass_out() -> void:
	_begin_next_day(config.passout_wake_minute, true)


func request_pause(source: StringName) -> void:
	var was_paused: bool = is_paused()
	_pause_sources[source] = true
	if not was_paused:
		EventBus.time_pause_changed.emit(true)


func release_pause(source: StringName) -> void:
	var was_paused: bool = is_paused()
	_pause_sources.erase(source)
	if was_paused and not is_paused():
		EventBus.time_pause_changed.emit(false)


func is_paused() -> bool:
	return not _pause_sources.is_empty()


# --- Abfragen --------------------------------------------------------------

func hour() -> int:
	@warning_ignore("integer_division")
	return (int(minute_of_day) / MINUTES_PER_HOUR) % 24


func minute() -> int:
	return int(minute_of_day) % MINUTES_PER_HOUR


func clock_text() -> String:
	return "%02d:%02d" % [hour(), minute()]


## Fortlaufender Tag seit Spielbeginn (Tag 1 = 1).
func absolute_day() -> int:
	return ((year - 1) * config.seasons_per_year + season) * config.days_per_season + day


## 0 = erster Wochentag (Montag).
func weekday() -> int:
	return (absolute_day() - 1) % config.days_per_week


func season_key() -> StringName:
	return SEASON_KEYS[season]


## Mondphase (0..7) für einen Tag der Jahreszeit (1..days_per_season).
func moon_phase_for_day(day_of_season: int) -> int:
	var remaining: int = (day_of_season - 1) % _moon_cycle_length()
	for phase: int in config.moon_phase_lengths.size():
		remaining -= config.moon_phase_lengths[phase]
		if remaining < 0:
			return phase
	return config.moon_phase_lengths.size() - 1


func moon_phase() -> int:
	return moon_phase_for_day(day)


func is_full_moon() -> bool:
	return moon_phase() == FULL_MOON_PHASE


## Fortschritt des Tages von 0.0 (Tagesbeginn) bis 1.0 (02:00), z. B. für Lichtrampen.
func day_progress() -> float:
	var span: float = float(config.day_end_minute - config.day_start_minute)
	return clampf((minute_of_day - config.day_start_minute) / span, 0.0, 1.0)


# --- Speichern -------------------------------------------------------------

func to_dict() -> Dictionary:
	return {
		"minute_of_day": minute_of_day,
		"day": day,
		"season": season,
		"year": year,
		"woke_from_passout": woke_from_passout,
	}


func from_dict(d: Dictionary) -> void:
	minute_of_day = float(d.get("minute_of_day", config.day_start_minute))
	day = int(d.get("day", 1))
	season = int(d.get("season", Season.SPRING))
	year = int(d.get("year", 1))
	woke_from_passout = bool(d.get("woke_from_passout", false))


# --- Intern ----------------------------------------------------------------

func _begin_next_day(wake_minute: int, passed_out: bool) -> void:
	EventBus.day_ended.emit(day, season, year)
	day += 1
	var season_changed: bool = false
	if day > config.days_per_season:
		day = 1
		season += 1
		season_changed = true
		if season >= config.seasons_per_year:
			season = Season.SPRING
			year += 1
	minute_of_day = float(wake_minute)
	woke_from_passout = passed_out
	if season_changed:
		EventBus.season_changed.emit(season, year)
	EventBus.day_started.emit(day, season, year)


## Entspannter Modus (Barrierefreiheit): Zeit läuft langsamer. Die Pause in
## Innenräumen melden Innenraum-Szenen ab M2 als Pausenquelle an.
func _apply_relaxed_mode() -> void:
	var relaxed: bool = bool(Settings.get_value("accessibility", "relaxed_mode"))
	time_scale = config.relaxed_mode_factor if relaxed else 1.0


func _on_settings_changed(section: StringName) -> void:
	if section == &"accessibility":
		_apply_relaxed_mode()


func _moon_cycle_length() -> int:
	var total: int = 0
	for length: int in config.moon_phase_lengths:
		total += length
	return maxi(total, 1)
