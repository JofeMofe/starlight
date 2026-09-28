class_name SizeChangeRules
extends RefCounted
## Wann darf Klio die Größe wechseln, und was kostet es? (§6.3)
## Kapitel 1: nur an Feenringen. Ab Kapitel 2 überall für Feenglanz.
## Ab Kapitel 4 überall kostenlos. An Feenringen immer kostenlos.

const REASON_OK: StringName = &""
const REASON_NEED_RING: StringName = &"hint.transform.need_ring"
const REASON_NO_GLOW: StringName = &"hint.transform.no_glow"


## Ergebnis: {"allowed": bool, "cost": float, "reason": StringName}
static func evaluate(chapter: int, at_fairy_ring: bool, glow: float, config: MovementConfig) -> Dictionary:
	if at_fairy_ring or chapter >= config.free_transform_chapter:
		return {"allowed": true, "cost": 0.0, "reason": REASON_OK}
	if chapter < config.anywhere_transform_chapter:
		return {"allowed": false, "cost": 0.0, "reason": REASON_NEED_RING}
	if glow < config.transform_glow_cost:
		return {"allowed": false, "cost": config.transform_glow_cost, "reason": REASON_NO_GLOW}
	return {"allowed": true, "cost": config.transform_glow_cost, "reason": REASON_OK}
