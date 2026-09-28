extends Node
## Globale Signale. Systeme kennen einander nicht direkt, sondern senden und
## empfangen über diesen Bus (lose Kopplung, siehe docs/ARCHITECTURE.md).
##
## Konvention: Vergangenheitsform ("etwas ist passiert"), Parameter typisiert.
## Die Signale werden von anderen Skripten ausgelöst, daher die Unterdrückung
## der "unused_signal"-Warnung.

@warning_ignore_start("unused_signal")

# --- Zeit & Kalender -------------------------------------------------------
signal minute_changed(minute_of_day: int)
signal hour_changed(hour: int)
signal day_started(day: int, season: int, year: int)
signal day_ended(day: int, season: int, year: int)
signal season_changed(season: int, year: int)
signal time_pause_changed(paused: bool)

# --- Wetter ----------------------------------------------------------------
signal weather_changed(weather: StringName)

# --- Spielerin & Welt ------------------------------------------------------
signal player_size_changed(player_id: int, is_fairy: bool)
signal glow_changed(player_id: int, value: float, max_value: float)
signal money_changed(player_id: int, value: int)
signal item_acquired(player_id: int, item_id: StringName, amount: int)

# --- Tiere & Beziehungen ---------------------------------------------------
signal animal_bond_changed(animal_id: StringName, value: float)
signal relationship_changed(npc_id: StringName, hearts: float)
signal heart_spring_changed(points: int, chapter: int)

# --- Feste & Story ---------------------------------------------------------
signal festival_started(festival_id: StringName)
signal flag_changed(flag: StringName, value: bool)

# --- Dialog ----------------------------------------------------------------
signal dialogue_started(dialogue_id: StringName)
signal dialogue_line_shown(speaker: StringName, text_key: String, emotion: StringName)
signal dialogue_ended(dialogue_id: StringName)

# --- Szenen, Speichern, Einstellungen --------------------------------------
signal scene_change_started(target_path: String)
signal scene_changed(scene_path: String, spawn_point: StringName)
signal game_saved(slot: String)
signal game_loaded(slot: String)
signal settings_changed(section: StringName)
signal locale_changed(locale: String)
signal input_device_changed(is_gamepad: bool)

@warning_ignore_restore("unused_signal")
