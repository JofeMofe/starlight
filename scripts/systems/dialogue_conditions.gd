class_name DialogueConditions
extends RefCounted
## Auswertung von Dialogbedingungen (rein, ohne Zustand -> leicht testbar).
##
## Kontext-Schlüssel: hearts, flags (Dictionary), hour, season, weather, dog_present.

## Prüft Bedingungen einer Zeile. Unbekannte Bedingungen gelten als nicht
## erfüllt, damit Tippfehler in Daten auffallen statt still durchzurutschen.
static func met(conditions: Dictionary, context: Dictionary) -> bool:
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
