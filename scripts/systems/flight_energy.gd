class_name FlightEnergy
extends RefCounted
## Flugenergie der Fee: sinkt beim Fliegen, lädt sich nach kurzer Pause
## schnell wieder auf. Leer heißt nur "sanft landen", nie Absturz (cozy).

var max_value: float
var value: float
var drain: float
var regen: float
var regen_delay: float

var _since_use: float = 0.0


func _init(p_max: float, p_drain: float, p_regen: float, p_regen_delay: float) -> void:
	max_value = p_max
	value = p_max
	drain = p_drain
	regen = p_regen
	regen_delay = p_regen_delay


## Verbraucht Energie für `delta` Sekunden Flug. Gibt false zurück, wenn leer.
func use(delta: float) -> bool:
	_since_use = 0.0
	value = maxf(0.0, value - drain * delta)
	return value > 0.0


func rest(delta: float) -> void:
	_since_use += delta
	if _since_use >= regen_delay:
		value = minf(max_value, value + regen * delta)


func ratio() -> float:
	return value / max_value if max_value > 0.0 else 0.0


func is_empty() -> bool:
	return value <= 0.0
