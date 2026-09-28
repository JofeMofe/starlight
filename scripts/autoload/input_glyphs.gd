extends Node
## Erkennt, ob zuletzt Tastatur/Maus oder Gamepad benutzt wurde, und liefert
## passende Tastenhinweise. Glyphen-Grafiken folgen mit dem UI (M2);
## bis dahin werden Textbezeichnungen zurückgegeben.

enum Family { KEYBOARD, XBOX, PLAYSTATION, NINTENDO }

const STICK_THRESHOLD: float = 0.5
const FACE_LABELS: Dictionary = {
	Family.XBOX: {"a": "A", "b": "B", "x": "X", "y": "Y", "lb": "LB", "rb": "RB", "start": "Menu", "back": "View"},
	Family.PLAYSTATION: {"a": "✕", "b": "○", "x": "□", "y": "△", "lb": "L1", "rb": "R1", "start": "Options", "back": "Share"},
	# Nintendo: Godot mappt nach Position, daher unten = "B", rechts = "A"
	Family.NINTENDO: {"a": "B", "b": "A", "x": "Y", "y": "X", "lb": "L", "rb": "R", "start": "+", "back": "−"},
}

var using_gamepad: bool = false
var family: Family = Family.KEYBOARD


func _input(event: InputEvent) -> void:
	var gamepad: bool = using_gamepad
	if event is InputEventKey or event is InputEventMouseButton:
		gamepad = false
	elif event is InputEventMouseMotion and (event as InputEventMouseMotion).relative.length() > 2.0:
		gamepad = false
	elif event is InputEventJoypadButton:
		gamepad = true
		_detect_family(event.device)
	elif event is InputEventJoypadMotion and absf((event as InputEventJoypadMotion).axis_value) > STICK_THRESHOLD:
		gamepad = true
		_detect_family(event.device)
	if gamepad != using_gamepad:
		using_gamepad = gamepad
		EventBus.input_device_changed.emit(using_gamepad)


## Bezeichnung der ersten passenden Belegung einer Aktion für das aktive Gerät.
func label_for(action: StringName) -> String:
	for binding: String in Settings.bindings(action):
		var kind: String = binding.get_slice(":", 0)
		var value: String = binding.substr(kind.length() + 1)
		if using_gamepad and kind == "joy_button":
			var labels: Dictionary = FACE_LABELS.get(family, FACE_LABELS[Family.XBOX]) as Dictionary
			return str(labels.get(value, value.to_upper()))
		if using_gamepad and kind == "joy_axis":
			return value.trim_suffix("+").trim_suffix("-").to_upper()
		if not using_gamepad and kind in ["key", "mouse"]:
			return value
	return "?"


func _detect_family(device: int) -> void:
	var joy_name: String = Input.get_joy_name(device).to_lower()
	if "playstation" in joy_name or "dualshock" in joy_name or "dualsense" in joy_name or "ps4" in joy_name or "ps5" in joy_name:
		family = Family.PLAYSTATION
	elif "nintendo" in joy_name or "switch" in joy_name or "joy-con" in joy_name:
		family = Family.NINTENDO
	else:
		family = Family.XBOX
