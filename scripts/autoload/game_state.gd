extends Node
## Spielstand im Speicher: Spielerinnen, Hofname, Flags und Herzquelle.
## Inventar, Tiere und Beziehungen kommen mit ihren Systemen (M2–M4) hinzu und
## registrieren sich hier über `to_dict()`/`from_dict()`.

const LOCAL_PLAYER_ID: int = 1

var players: Dictionary[int, PlayerData] = {}
var farm_name: String = ""
var soul_dog_id: StringName = &""
var heart_spring_points: int = 0
var heart_spring_chapter: int = 1
var flags: Dictionary[StringName, bool] = {}
## Gespielte Zeit in Sekunden (für Speicherstand-Anzeige).
var play_time_seconds: float = 0.0


func _init() -> void:
	reset()


func _process(delta: float) -> void:
	play_time_seconds += delta


func reset() -> void:
	players.clear()
	var klio: PlayerData = PlayerData.new()
	klio.player_id = LOCAL_PLAYER_ID
	players[LOCAL_PLAYER_ID] = klio
	farm_name = ""
	soul_dog_id = &""
	heart_spring_points = 0
	heart_spring_chapter = 1
	flags.clear()
	play_time_seconds = 0.0


func local_player() -> PlayerData:
	return players[LOCAL_PLAYER_ID]


func player(player_id: int) -> PlayerData:
	return players.get(player_id) as PlayerData


func set_flag(flag: StringName, value: bool = true) -> void:
	if flags.get(flag, false) == value:
		return
	flags[flag] = value
	EventBus.flag_changed.emit(flag, value)


func has_flag(flag: StringName) -> bool:
	return flags.get(flag, false)


func add_money(player_id: int, amount: int) -> void:
	var p: PlayerData = player(player_id)
	p.money = maxi(0, p.money + amount)
	EventBus.money_changed.emit(player_id, p.money)


func to_dict() -> Dictionary:
	var player_dicts: Array[Dictionary] = []
	for p: PlayerData in players.values():
		player_dicts.append(p.to_dict())
	var flag_dict: Dictionary = {}
	for f: StringName in flags:
		flag_dict[String(f)] = flags[f]
	return {
		"players": player_dicts,
		"farm_name": farm_name,
		"soul_dog_id": String(soul_dog_id),
		"heart_spring_points": heart_spring_points,
		"heart_spring_chapter": heart_spring_chapter,
		"flags": flag_dict,
		"play_time_seconds": play_time_seconds,
	}


func from_dict(d: Dictionary) -> void:
	reset()
	players.clear()
	for pd: Variant in d.get("players", []) as Array:
		var p: PlayerData = PlayerData.new()
		p.from_dict(pd as Dictionary)
		players[p.player_id] = p
	if not players.has(LOCAL_PLAYER_ID):
		var klio: PlayerData = PlayerData.new()
		players[LOCAL_PLAYER_ID] = klio
	farm_name = str(d.get("farm_name", ""))
	soul_dog_id = StringName(str(d.get("soul_dog_id", "")))
	heart_spring_points = int(d.get("heart_spring_points", 0))
	heart_spring_chapter = int(d.get("heart_spring_chapter", 1))
	var flag_dict: Dictionary = d.get("flags", {}) as Dictionary
	for key: Variant in flag_dict:
		flags[StringName(str(key))] = bool(flag_dict[key])
	play_time_seconds = float(d.get("play_time_seconds", 0.0))
