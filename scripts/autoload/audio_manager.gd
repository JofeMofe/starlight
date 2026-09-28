extends Node
## Musik mit Crossfade, Ambience-Layer, SFX-Pool mit leichter Zufallsvariation
## und szenenabhängiger Hall (Innenräume, Mikro-Areale).

const DEFAULT_CROSSFADE: float = 3.0
const SFX_POOL_SIZE: int = 16
const SILENT_DB: float = -60.0
const SFX_BUS: StringName = &"SFX"
const REVERB_BUSES: Array[StringName] = [&"SFX", &"Ambience"]

var _music_a: AudioStreamPlayer
var _music_b: AudioStreamPlayer
var _active_music: AudioStreamPlayer
var _ambience: Dictionary[StringName, AudioStreamPlayer] = {}
var _sfx_pool: Array[AudioStreamPlayer] = []
var _sfx_next: int = 0
var _rng: RandomNumberGenerator = RandomNumberGenerator.new()


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_music_a = _make_player(&"Music", "MusicA")
	_music_b = _make_player(&"Music", "MusicB")
	_active_music = _music_a
	for i: int in SFX_POOL_SIZE:
		_sfx_pool.append(_make_player(SFX_BUS, "Sfx%d" % i))
	_rng.randomize()


## Blendet zu einem neuen Musikstück über. Gleiches Stück läuft einfach weiter.
func play_music(stream: AudioStream, fade_seconds: float = DEFAULT_CROSSFADE) -> void:
	if _active_music.stream == stream and _active_music.playing:
		return
	var old: AudioStreamPlayer = _active_music
	var new: AudioStreamPlayer = _music_b if old == _music_a else _music_a
	new.stream = stream
	new.volume_db = SILENT_DB
	new.play()
	_active_music = new
	var tween: Tween = create_tween().set_parallel(true)
	tween.tween_property(new, "volume_db", 0.0, fade_seconds).set_trans(Tween.TRANS_SINE)
	tween.tween_property(old, "volume_db", SILENT_DB, fade_seconds).set_trans(Tween.TRANS_SINE)
	tween.chain().tween_callback(old.stop)


func stop_music(fade_seconds: float = DEFAULT_CROSSFADE) -> void:
	var player: AudioStreamPlayer = _active_music
	var tween: Tween = create_tween()
	tween.tween_property(player, "volume_db", SILENT_DB, fade_seconds)
	tween.tween_callback(player.stop)


## Setzt einen benannten Ambience-Layer (z. B. &"rain", &"birds"); null entfernt ihn.
func set_ambience(layer: StringName, stream: AudioStream, volume_db: float = 0.0, fade_seconds: float = 2.0) -> void:
	var player: AudioStreamPlayer = _ambience.get(layer) as AudioStreamPlayer
	if stream == null:
		if player != null:
			var t: Tween = create_tween()
			t.tween_property(player, "volume_db", SILENT_DB, fade_seconds)
			t.tween_callback(player.queue_free)
			_ambience.erase(layer)
		return
	if player == null:
		player = _make_player(&"Ambience", "Amb_%s" % layer)
		_ambience[layer] = player
		player.volume_db = SILENT_DB
	if player.stream != stream:
		player.stream = stream
		player.play()
	create_tween().tween_property(player, "volume_db", volume_db, fade_seconds)


## Spielt einen Soundeffekt mit leichter Tonhöhen-/Lautstärkevariation,
## damit Wiederholungen (Schritte, Klicks) nicht mechanisch klingen.
func play_sfx(stream: AudioStream, volume_db: float = 0.0, pitch_variation: float = 0.05,
		bus: StringName = SFX_BUS, pitch: float = 1.0) -> void:
	if stream == null:
		return
	var player: AudioStreamPlayer = _sfx_pool[_sfx_next]
	_sfx_next = (_sfx_next + 1) % _sfx_pool.size()
	player.bus = bus
	player.stream = stream
	player.pitch_scale = pitch * (1.0 + _rng.randf_range(-pitch_variation, pitch_variation))
	player.volume_db = volume_db + _rng.randf_range(-1.0, 1.0)
	player.play()


## Hall für Innenräume/Mikro-Areale ein- oder ausschalten.
func set_indoor_reverb(enabled: bool) -> void:
	for bus: StringName in REVERB_BUSES:
		var idx: int = AudioServer.get_bus_index(bus)
		if idx >= 0 and AudioServer.get_bus_effect_count(idx) > 0:
			AudioServer.set_bus_effect_enabled(idx, 0, enabled)


func _make_player(bus: StringName, node_name: String) -> AudioStreamPlayer:
	var p: AudioStreamPlayer = AudioStreamPlayer.new()
	p.name = node_name
	p.bus = bus
	add_child(p)
	return p
