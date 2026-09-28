extends Node
## Dünner Wrapper um TranslationServer. Texte liegen als Schlüssel in
## data/localization/*.csv (Spalten: keys, de, en) und werden von Godot beim
## Import zu .translation-Dateien (in project.godot registriert).
## Deutsch ist Primärsprache und Fallback.

const SUPPORTED_LOCALES: PackedStringArray = ["de", "en"]
const DEFAULT_LOCALE: String = "de"


func _ready() -> void:
	set_locale(str(Settings.get_value("general", "locale")))


func set_locale(locale: String) -> void:
	var target: String = locale if locale in SUPPORTED_LOCALES else DEFAULT_LOCALE
	TranslationServer.set_locale(target)
	EventBus.locale_changed.emit(target)


func current_locale() -> String:
	return TranslationServer.get_locale().left(2)


## Übersetzt einen Schlüssel und setzt {platzhalter} aus `vars` ein.
func text(key: String, vars: Dictionary = {}) -> String:
	var result: String = TranslationServer.translate(key)
	return result.format(vars) if not vars.is_empty() else result


## true, wenn der Schlüssel in der aktuellen Sprache übersetzt ist.
func has_key(key: String) -> bool:
	return TranslationServer.translate(key) != key
