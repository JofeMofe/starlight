class_name Interactable
extends Area2D
## Etwas, mit dem Klio interagieren kann. Der Besitzer liefert die Hinweise
## (Übersetzungsschlüssel) passend zur Situation über `prompt_provider` und
## reagiert auf die Signale. Primär = Interagieren (E/A), sekundär = Leertaste/B.

signal interacted(actor: Node2D)
signal interacted_secondary(actor: Node2D)

## Callable(actor: Node2D) -> Dictionary {"primary": String, "secondary": String}
## Leerer String = diese Aktion ist gerade nicht möglich.
var prompt_provider: Callable = Callable()
@export var enabled: bool = true
@export var focus_priority: int = 0


func _ready() -> void:
	collision_layer = PhysicsLayers.INTERACT
	collision_mask = 0
	monitoring = false
	monitorable = true


func prompts_for(actor: Node2D) -> Dictionary:
	if not enabled or not prompt_provider.is_valid():
		return {"primary": "", "secondary": ""}
	return prompt_provider.call(actor) as Dictionary


func interact(actor: Node2D) -> void:
	if enabled:
		interacted.emit(actor)


func interact_secondary(actor: Node2D) -> void:
	if enabled:
		interacted_secondary.emit(actor)
