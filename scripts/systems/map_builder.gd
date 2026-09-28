class_name MapBuilder
extends RefCounted
## Baut eine Karte aus Daten (§1.8): ASCII-Raster (data/maps/*.json) plus
## Kachelsatz-Beschreibung (data/tilesets/*.json). Wählt Kantenvarianten per
## Nachbar-Bitmaske (N=1, O=2, S=4, W=8), legt Kollisionen an, setzt Objekte
## und liefert die Startpunkte. Neue Karten brauchen keinen Code.

const N: int = 1
const E: int = 2
const S: int = 4
const W: int = 8
const DIRS: Array[Vector2i] = [Vector2i(0, -1), Vector2i(1, 0), Vector2i(0, 1), Vector2i(-1, 0)]
const WALL_THICKNESS: float = 64.0

var map_data: Dictionary = {}
var tiles_data: Dictionary = {}
var tile_set: TileSet
var tile_size: int = 32
var size: Vector2i = Vector2i.ZERO
var spawns: Dictionary[StringName, Vector2] = {}

var _rows: PackedStringArray = []
var _legend: Dictionary = {}
var _source_id: int = -1


func _init(map_path: String) -> void:
	map_data = _load_json(map_path)
	tiles_data = _load_json(str(map_data.get("tileset", "")))
	tile_size = int(tiles_data.get("tile_size", 32))
	var sz: Array = map_data.get("size", [0, 0]) as Array
	size = Vector2i(int(sz[0]), int(sz[1]))
	_rows = PackedStringArray(map_data.get("rows", []) as Array)
	_legend = map_data.get("legend", {}) as Dictionary
	tile_set = _build_tileset()


func pixel_size() -> Vector2i:
	return size * tile_size


## Füllt Boden- und Objektebene, platziert Objekte und Randwände.
func build(ground: TileMapLayer, objects_layer: TileMapLayer, objects_parent: Node2D, deco_parent: Node2D,
		walls: StaticBody2D) -> void:
	ground.tile_set = tile_set
	objects_layer.tile_set = tile_set
	var terrains: Dictionary = tiles_data.get("terrains", {}) as Dictionary
	for y: int in size.y:
		for x: int in size.x:
			var cell: Vector2i = Vector2i(x, y)
			var kind: String = kind_at(cell)
			ground.set_cell(cell, _source_id, Vector2i(_grass_variant(cell), int((terrains["grass"] as Dictionary)["row"])))
			if kind.begins_with("object:") or kind.begins_with("deco:") or kind.begins_with("ring:"):
				_place_object(kind, cell, objects_parent, deco_parent)
				continue
			if kind.begins_with("spawn:"):
				spawns[StringName(kind.get_slice(":", 1))] = cell_to_feet(cell)
				continue
			if not terrains.has(kind) or kind == "grass":
				continue
			var t: Dictionary = terrains[kind] as Dictionary
			var coords: Vector2i = Vector2i(mask_at(cell, kind), int(t["row"]))
			if str(t.get("layer", "ground")) == "objects":
				objects_layer.set_cell(cell, _source_id, coords)
			else:
				ground.set_cell(cell, _source_id, coords)
	_scatter(objects_parent, deco_parent)
	if bool(map_data.get("border_trees", false)):
		_place_border_trees(objects_parent)
	_build_walls(walls)


func kind_at(cell: Vector2i) -> String:
	if cell.y < 0 or cell.y >= _rows.size() or cell.x < 0 or cell.x >= _rows[cell.y].length():
		return ""
	return str(_legend.get(_rows[cell.y][cell.x], "grass"))


## Bitmaske der gleichartigen Nachbarn. Außerhalb der Karte zählt als gleich,
## damit am Kartenrand keine falschen Ufer/Wegenden entstehen.
func mask_at(cell: Vector2i, kind: String) -> int:
	var m: int = 0
	for i: int in DIRS.size():
		var n: Vector2i = cell + DIRS[i]
		var outside: bool = n.x < 0 or n.y < 0 or n.x >= size.x or n.y >= size.y
		if outside or kind_at(n) == kind:
			m |= 1 << i
	return m


func cell_to_feet(cell: Vector2i) -> Vector2:
	return Vector2(cell.x * tile_size + tile_size * 0.5, cell.y * tile_size + tile_size - 4)


func cell_center(cell: Vector2i) -> Vector2:
	return Vector2(cell) * tile_size + Vector2.ONE * tile_size * 0.5


# --- Kachelsatz -------------------------------------------------------------

func _build_tileset() -> TileSet:
	var ts: TileSet = TileSet.new()
	ts.tile_size = Vector2i(tile_size, tile_size)
	ts.add_physics_layer()
	ts.set_physics_layer_collision_layer(0, PhysicsLayers.SOLID_LOW)
	ts.set_physics_layer_collision_mask(0, 0)
	var src: TileSetAtlasSource = TileSetAtlasSource.new()
	src.texture = load(str(tiles_data["texture"])) as Texture2D
	src.texture_region_size = Vector2i(tile_size, tile_size)
	_source_id = ts.add_source(src)
	var terrains: Dictionary = tiles_data.get("terrains", {}) as Dictionary
	for key: Variant in terrains:
		var t: Dictionary = terrains[key] as Dictionary
		var row: int = int(t["row"])
		var count: int = 16 if bool(t.get("mask", false)) else int(t.get("variants", 1))
		for col: int in count:
			var coords: Vector2i = Vector2i(col, row)
			src.create_tile(coords)
			var td: TileData = src.get_tile_data(coords, 0)
			if bool(t.get("fence", false)):
				td.y_sort_origin = 8
				for poly: PackedVector2Array in _fence_polygons(col):
					_add_polygon(td, poly)
			elif str(t.get("collision", "")) != "":
				_add_polygon(td, _inset_rect(col, float(t.get("inset", 0))))
	return ts


func _add_polygon(td: TileData, points: PackedVector2Array) -> void:
	td.add_collision_polygon(0)
	td.set_collision_polygon_points(0, td.get_collision_polygons_count(0) - 1, points)


## Rechteck über die ganze Kachel, an offenen Seiten (kein gleicher Nachbar) eingerückt.
func _inset_rect(mask: int, inset: float) -> PackedVector2Array:
	var h: float = tile_size * 0.5
	var l: float = -h + (0.0 if mask & W else inset)
	var r: float = h - (0.0 if mask & E else inset)
	var t: float = -h + (0.0 if mask & N else inset)
	var b: float = h - (0.0 if mask & S else inset)
	return PackedVector2Array([Vector2(l, t), Vector2(r, t), Vector2(r, b), Vector2(l, b)])


## Zaun: Pfosten plus Latten zu verbundenen Nachbarn, nur im Fußbereich,
## damit Figuren hinter dem Zaun (weiter oben) nicht anstoßen.
func _fence_polygons(mask: int) -> Array[PackedVector2Array]:
	var h: float = tile_size * 0.5
	var polys: Array[PackedVector2Array] = [_rect(-5, 2, 5, 11)]
	if mask & E:
		polys.append(_rect(0, 3, h, 10))
	if mask & W:
		polys.append(_rect(-h, 3, 0, 10))
	if mask & N:
		polys.append(_rect(-3, -h, 3, 10))
	if mask & S:
		polys.append(_rect(-3, 2, 3, h))
	return polys


func _rect(l: float, t: float, r: float, b: float) -> PackedVector2Array:
	return PackedVector2Array([Vector2(l, t), Vector2(r, t), Vector2(r, b), Vector2(l, b)])


# --- Objekte ----------------------------------------------------------------

func _place_object(kind: String, cell: Vector2i, objects_parent: Node2D, deco_parent: Node2D) -> void:
	var key: String = kind.get_slice(":", 1)
	var objects: Dictionary = tiles_data.get("objects", {}) as Dictionary
	if not objects.has(key):
		push_error("MapBuilder: Objekt '%s' fehlt in %s" % [key, map_data.get("tileset", "")])
		return
	var scene: PackedScene = load(str(objects[key])) as PackedScene
	var node: Node2D = scene.instantiate() as Node2D
	node.name = "%s_%d_%d" % [key, cell.x, cell.y]
	if kind.begins_with("object:"):
		node.position = cell_to_feet(cell)
		objects_parent.add_child(node)
	else:
		node.position = cell_center(cell)
		deco_parent.add_child(node)


## Verstreut Deko (hohes Gras, Kiesel, Blumen) auf freien Graskacheln.
## Deterministisch über den Zellen-Hash: gleiche Karte = gleiche Wiese.
func _scatter(objects_parent: Node2D, deco_parent: Node2D) -> void:
	var rules: Array = map_data.get("scatter", []) as Array
	for y: int in range(1, size.y - 1):
		for x: int in range(1, size.x - 1):
			var cell: Vector2i = Vector2i(x, y)
			if kind_at(cell) != "grass":
				continue
			for i: int in rules.size():
				var rule: Dictionary = rules[i] as Dictionary
				var roll: float = float(absi(hash([cell, i, "scatter"])) % 10000) / 10000.0
				if roll < float(rule.get("chance", 0.0)):
					var prefix: String = "deco:" if bool(rule.get("deco", false)) else "object:"
					_place_object(prefix + str(rule["object"]), cell, objects_parent, deco_parent)
					break


func _place_border_trees(parent: Node2D) -> void:
	var objects: Dictionary = tiles_data.get("objects", {}) as Dictionary
	var scene: PackedScene = load(str(objects["tree"])) as PackedScene
	var cells: Array[Vector2i] = []
	for x: int in range(0, size.x, 2):
		cells.append(Vector2i(x, 0))
		cells.append(Vector2i(x + 1, size.y - 1))
	for y: int in range(2, size.y - 1, 2):
		cells.append(Vector2i(0, y))
		cells.append(Vector2i(size.x - 1, y - 1))
	for cell: Vector2i in cells:
		var tree: Node2D = scene.instantiate() as Node2D
		tree.name = "border_tree_%d_%d" % [cell.x, cell.y]
		tree.position = cell_to_feet(cell)
		parent.add_child(tree)


func _build_walls(walls: StaticBody2D) -> void:
	walls.collision_layer = PhysicsLayers.SOLID_HIGH
	walls.collision_mask = 0
	var px: Vector2 = Vector2(pixel_size())
	var t: float = WALL_THICKNESS
	for rect: Rect2 in [Rect2(-t, -t, px.x + 2 * t, t), Rect2(-t, px.y, px.x + 2 * t, t),
			Rect2(-t, 0, t, px.y), Rect2(px.x, 0, t, px.y)]:
		var shape: RectangleShape2D = RectangleShape2D.new()
		shape.size = rect.size
		var col: CollisionShape2D = CollisionShape2D.new()
		col.shape = shape
		col.position = rect.position + rect.size * 0.5
		walls.add_child(col)


func _grass_variant(cell: Vector2i) -> int:
	# Deterministisch gestreut; Variante 0 am häufigsten, Blumen selten
	var h: int = absi(hash(cell)) % 100
	if h < 55:
		return 0
	if h < 80:
		return 1
	if h < 90:
		return 3
	return 2


static func _load_json(path: String) -> Dictionary:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if parsed is not Dictionary:
		push_error("MapBuilder: %s ungültig" % path)
		return {}
	return parsed as Dictionary
