extends Node2D
## Feenring (§6.3): Hier verwandelt sich Klio im frühen Spiel, und immer
## kostenlos. Interagieren (E) löst die Verwandlung direkt aus.

const SFX_HUM: AudioStream = preload("res://assets/audio/sfx/ring_hum.ogg")

@onready var _interact: Interactable = $Interactable


func _ready() -> void:
	add_to_group(&"fairy_rings")
	_interact.prompt_provider = _prompts
	_interact.interacted.connect(_on_interacted)


func _prompts(actor: Node2D) -> Dictionary:
	var klio: Klio = actor as Klio
	if klio == null:
		return {"primary": "", "secondary": ""}
	return {"primary": "prompt.ring.to_human" if klio.is_fairy else "prompt.ring.to_fairy", "secondary": ""}


func _on_interacted(actor: Node2D) -> void:
	var klio: Klio = actor as Klio
	if klio != null and klio.try_toggle_size():
		AudioManager.play_sfx(SFX_HUM, -6.0, 0.0)
