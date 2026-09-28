class_name TimeConfig
extends Resource
## Taktung von Uhr und Kalender. Instanz: res://data/config/time.tres

## Tagesbeginn in Minuten seit Mitternacht (06:00).
@export var day_start_minute: int = 360
## Automatisches Einschlafen in Minuten seit Mitternacht des Tages (02:00 = 26 * 60).
@export var day_end_minute: int = 1560
## Echtzeit-Sekunden pro Spielminute. 0.7 -> 10 Spielminuten = 7 s, ein Tag ≈ 14 min.
@export var real_seconds_per_game_minute: float = 0.7
## Im "Entspannten Modus" läuft die Zeit um diesen Faktor langsamer.
@export var relaxed_mode_factor: float = 0.5
## Aufwachzeit nach Einschlafen um 02:00 (etwas später, cozy statt Strafe).
@export var passout_wake_minute: int = 420
## Anteil des maximalen Feenglanzes nach Einschlafen um 02:00.
@export var passout_glow_ratio: float = 0.8
@export var days_per_season: int = 28
@export var seasons_per_year: int = 4
@export var days_per_week: int = 7
## Länge jeder der 8 Mondphasen in Tagen; Summe = Mondzyklus (28, synchron zur Jahreszeit).
## Neumond, zun. Sichel, erstes Viertel, zun. Mond, Vollmond, abn. Mond, letztes Viertel, abn. Sichel.
@export var moon_phase_lengths: PackedInt32Array = PackedInt32Array([1, 6, 1, 6, 1, 6, 1, 6])
