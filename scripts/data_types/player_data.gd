class_name PlayerData
extends RefCounted
## Zustand einer Spielerin. Über `player_id` adressiert, damit späterer Koop
## (§7.15) mehrere Instanzen halten kann, ohne ein globales Unikat anzunehmen.

const DEFAULT_MAX_GLOW: float = 100.0

var player_id: int = 1
## Die Heldin ist immer Klio (§5.1); der Name ist fest und nicht editierbar.
var character_name: String = "Klio"
var money: int = 0
var glow: float = DEFAULT_MAX_GLOW
var max_glow: float = DEFAULT_MAX_GLOW
var is_fairy: bool = false
var scene_path: String = ""
var position: Vector2 = Vector2.ZERO


func to_dict() -> Dictionary:
	return {
		"player_id": player_id,
		"character_name": character_name,
		"money": money,
		"glow": glow,
		"max_glow": max_glow,
		"is_fairy": is_fairy,
		"scene_path": scene_path,
		"position": [position.x, position.y],
	}


func from_dict(d: Dictionary) -> void:
	player_id = int(d.get("player_id", 1))
	character_name = str(d.get("character_name", "Klio"))
	money = int(d.get("money", 0))
	max_glow = float(d.get("max_glow", DEFAULT_MAX_GLOW))
	glow = clampf(float(d.get("glow", max_glow)), 0.0, max_glow)
	is_fairy = bool(d.get("is_fairy", false))
	scene_path = str(d.get("scene_path", ""))
	var pos: Array = d.get("position", [0.0, 0.0]) as Array
	position = Vector2(float(pos[0]), float(pos[1])) if pos.size() == 2 else Vector2.ZERO
