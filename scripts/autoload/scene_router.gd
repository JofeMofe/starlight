extends Node
## Szenenwechsel mit Übergangseffekt und Spawnpunkten.
##
## Aufruf: `SceneRouter.goto("res://scenes/world/hof.tscn", &"from_village")`.
## Die Zielszene fragt `SceneRouter.pending_spawn` ab und platziert die
## Spielerin am Marker2D mit diesem Namen in der Gruppe "spawn_points".
## Der Feenstaub-Wipe (Shader) ersetzt in M2 die einfache Blende.

const FADE_SECONDS: float = 0.35
const OVERLAY_LAYER: int = 100
## Farbe der Blende: dunkelstes Palettenviolett (#1a1423).
const FADE_COLOR: Color = Color(0.101961, 0.0784314, 0.137255, 1.0)

var pending_spawn: StringName = &""
var is_transitioning: bool = false

var _overlay: ColorRect


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	var layer: CanvasLayer = CanvasLayer.new()
	layer.layer = OVERLAY_LAYER
	add_child(layer)
	_overlay = ColorRect.new()
	_overlay.color = FADE_COLOR
	_overlay.modulate.a = 0.0
	_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	layer.add_child(_overlay)


func goto(scene_path: String, spawn_point: StringName = &"", fade: bool = true) -> void:
	if is_transitioning:
		push_warning("SceneRouter: Wechsel zu %s ignoriert, Übergang läuft bereits" % scene_path)
		return
	if not ResourceLoader.exists(scene_path):
		push_error("SceneRouter: Szene %s existiert nicht" % scene_path)
		return
	is_transitioning = true
	pending_spawn = spawn_point
	EventBus.scene_change_started.emit(scene_path)
	if fade:
		await _fade_to(1.0)
	var err: Error = get_tree().change_scene_to_file(scene_path)
	if err != OK:
		push_error("SceneRouter: Laden von %s fehlgeschlagen (%s)" % [scene_path, error_string(err)])
		if fade:
			await _fade_to(0.0)
		is_transitioning = false
		return
	# change_scene_to_file tauscht die Szene erst am Ende des Frames aus.
	while get_tree().current_scene == null or get_tree().current_scene.scene_file_path != scene_path:
		await get_tree().process_frame
	EventBus.scene_changed.emit(scene_path, spawn_point)
	if fade:
		await _fade_to(0.0)
	is_transitioning = false


## Sucht in der aktuellen Szene den Spawnpunkt (Marker2D in Gruppe "spawn_points").
func find_spawn(scene_root: Node, spawn_name: StringName) -> Marker2D:
	for node: Node in scene_root.get_tree().get_nodes_in_group(&"spawn_points"):
		if node.name == spawn_name and scene_root.is_ancestor_of(node):
			return node as Marker2D
	return null


func _fade_to(alpha: float) -> void:
	var tween: Tween = create_tween()
	tween.tween_property(_overlay, "modulate:a", alpha, FADE_SECONDS).set_trans(Tween.TRANS_SINE)
	await tween.finished
