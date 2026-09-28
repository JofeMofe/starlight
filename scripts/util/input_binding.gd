class_name InputBinding
extends RefCounted
## Übersetzt zwischen kompakten Bindungs-Strings ("key:W", "joy_axis:left_y-")
## und InputEvents. Das Format ist menschenlesbar, damit Standardbelegung und
## gespeicherte Überschreibungen in Daten statt Code stehen.

const JOY_BUTTONS: Dictionary[String, JoyButton] = {
	"a": JOY_BUTTON_A, "b": JOY_BUTTON_B, "x": JOY_BUTTON_X, "y": JOY_BUTTON_Y,
	"back": JOY_BUTTON_BACK, "start": JOY_BUTTON_START, "guide": JOY_BUTTON_GUIDE,
	"ls": JOY_BUTTON_LEFT_STICK, "rs": JOY_BUTTON_RIGHT_STICK,
	"lb": JOY_BUTTON_LEFT_SHOULDER, "rb": JOY_BUTTON_RIGHT_SHOULDER,
	"dpad_up": JOY_BUTTON_DPAD_UP, "dpad_down": JOY_BUTTON_DPAD_DOWN,
	"dpad_left": JOY_BUTTON_DPAD_LEFT, "dpad_right": JOY_BUTTON_DPAD_RIGHT,
}
const JOY_AXES: Dictionary[String, JoyAxis] = {
	"left_x": JOY_AXIS_LEFT_X, "left_y": JOY_AXIS_LEFT_Y,
	"right_x": JOY_AXIS_RIGHT_X, "right_y": JOY_AXIS_RIGHT_Y,
	"lt": JOY_AXIS_TRIGGER_LEFT, "rt": JOY_AXIS_TRIGGER_RIGHT,
}
const MOUSE_BUTTONS: Dictionary[String, MouseButton] = {
	"left": MOUSE_BUTTON_LEFT, "right": MOUSE_BUTTON_RIGHT, "middle": MOUSE_BUTTON_MIDDLE,
	"wheel_up": MOUSE_BUTTON_WHEEL_UP, "wheel_down": MOUSE_BUTTON_WHEEL_DOWN,
}


## Wandelt einen Bindungs-String in ein InputEvent um (null bei ungültigem String).
static func to_event(binding: String) -> InputEvent:
	var kind: String = binding.get_slice(":", 0)
	var value: String = binding.substr(kind.length() + 1)
	match kind:
		"key":
			var code: Key = OS.find_keycode_from_string(value)
			if code == KEY_NONE:
				return null
			var key: InputEventKey = InputEventKey.new()
			key.physical_keycode = code
			return key
		"mouse":
			if not MOUSE_BUTTONS.has(value):
				return null
			var mb: InputEventMouseButton = InputEventMouseButton.new()
			mb.button_index = MOUSE_BUTTONS[value]
			return mb
		"joy_button":
			if not JOY_BUTTONS.has(value):
				return null
			var jb: InputEventJoypadButton = InputEventJoypadButton.new()
			jb.button_index = JOY_BUTTONS[value]
			return jb
		"joy_axis":
			var axis_name: String = value.left(value.length() - 1)
			var sign_char: String = value.right(1)
			if not JOY_AXES.has(axis_name) or sign_char not in ["+", "-"]:
				return null
			var jm: InputEventJoypadMotion = InputEventJoypadMotion.new()
			jm.axis = JOY_AXES[axis_name]
			jm.axis_value = 1.0 if sign_char == "+" else -1.0
			return jm
	return null


## Gegenrichtung zu to_event(); leerer String, falls das Event nicht abbildbar ist.
static func from_event(event: InputEvent) -> String:
	if event is InputEventKey:
		var key: InputEventKey = event as InputEventKey
		var code: Key = key.physical_keycode if key.physical_keycode != KEY_NONE else key.keycode
		return "key:" + OS.get_keycode_string(code)
	if event is InputEventMouseButton:
		var name: Variant = MOUSE_BUTTONS.find_key((event as InputEventMouseButton).button_index)
		return "mouse:" + str(name) if name != null else ""
	if event is InputEventJoypadButton:
		var name_b: Variant = JOY_BUTTONS.find_key((event as InputEventJoypadButton).button_index)
		return "joy_button:" + str(name_b) if name_b != null else ""
	if event is InputEventJoypadMotion:
		var jm: InputEventJoypadMotion = event as InputEventJoypadMotion
		var name_a: Variant = JOY_AXES.find_key(jm.axis)
		if name_a == null:
			return ""
		return "joy_axis:%s%s" % [name_a, "+" if jm.axis_value > 0.0 else "-"]
	return ""
