extends Node
## Datengetriebene Dialoge (Gerüst, voll ausgebaut in M4).
##
## Format (data/dialogue/<id>.json):
## {
##   "id": "frida_greeting",
##   "lines": [
##     {"speaker": "frida", "text": "dlg.frida.greeting.1", "emotion": "happy",
##      "if": {"season": "spring", "min_hearts": 2, "flag": "met_frida", "dog_present": true}}
##   ]
## }
## Texte sind Übersetzungsschlüssel; {dog_name}, {farm_name} usw. werden aus
## dem Kontext eingesetzt. Während eines Dialogs steht die Spielzeit still.

const DIALOGUE_DIR: String = "res://data/dialogue"
const PAUSE_SOURCE: StringName = &"dialogue"

var active_id: StringName = &""
var _lines: Array[Dictionary] = []
var _index: int = -1
var _context: Dictionary = {}


func is_active() -> bool:
	return active_id != &""


func load_dialogue(dialogue_id: StringName) -> Dictionary:
	var path: String = "%s/%s.json" % [DIALOGUE_DIR, dialogue_id]
	if not FileAccess.file_exists(path):
		push_error("DialogueManager: %s fehlt" % path)
		return {}
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	return parsed as Dictionary if parsed is Dictionary else {}


## Startet einen Dialog. `context` enthält Bedingungswerte und Variablen.
func start(dialogue_id: StringName, context: Dictionary = {}) -> bool:
	var data: Dictionary = load_dialogue(dialogue_id)
	if data.is_empty():
		return false
	_lines.clear()
	for line: Variant in data.get("lines", []) as Array:
		var d: Dictionary = line as Dictionary
		if conditions_met(d.get("if", {}) as Dictionary, context):
			_lines.append(d)
	if _lines.is_empty():
		return false
	active_id = dialogue_id
	_context = context
	_index = -1
	TimeManager.request_pause(PAUSE_SOURCE)
	EventBus.dialogue_started.emit(active_id)
	advance()
	return true


## Zeigt die nächste Zeile oder beendet den Dialog.
func advance() -> void:
	if not is_active():
		return
	_index += 1
	if _index >= _lines.size():
		end()
		return
	var line: Dictionary = _lines[_index]
	EventBus.dialogue_line_shown.emit(
		StringName(str(line.get("speaker", ""))),
		str(line.get("text", "")),
		StringName(str(line.get("emotion", "neutral"))))


func end() -> void:
	if not is_active():
		return
	var finished: StringName = active_id
	active_id = &""
	_lines.clear()
	_index = -1
	TimeManager.release_pause(PAUSE_SOURCE)
	EventBus.dialogue_ended.emit(finished)


## Übersetzt eine Zeile und setzt Kontextvariablen ein.
func render_text(text_key: String) -> String:
	return Localization.text(text_key, _context)


## Prüft Bedingungen einer Zeile. Unbekannte Bedingungen gelten als nicht
## erfüllt, damit Tippfehler in Daten auffallen statt still durchzurutschen.
static func conditions_met(conditions: Dictionary, context: Dictionary) -> bool:
	for key: Variant in conditions:
		var expected: Variant = conditions[key]
		match str(key):
			"min_hearts":
				if float(context.get("hearts", 0.0)) < float(expected):
					return false
			"max_hearts":
				if float(context.get("hearts", 0.0)) > float(expected):
					return false
			"flag":
				var flags: Dictionary = context.get("flags", {}) as Dictionary
				if not bool(flags.get(str(expected), false)):
					return false
			"not_flag":
				var flags_n: Dictionary = context.get("flags", {}) as Dictionary
				if bool(flags_n.get(str(expected), false)):
					return false
			"min_hour":
				if int(context.get("hour", 0)) < int(expected):
					return false
			"max_hour":
				if int(context.get("hour", 0)) > int(expected):
					return false
			"season", "weather", "dog_present":
				if context.get(str(key)) != expected:
					return false
			_:
				push_warning("DialogueManager: unbekannte Bedingung '%s'" % key)
				return false
	return true
