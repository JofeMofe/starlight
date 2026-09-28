extends Node2D
## Test-Wiese (M1): baut die Karte aus data/maps/test_meadow.json, backt das
## Navigationsnetz, setzt Klio, Hund und Pferd an ihre Startpunkte und
## verbindet Kamera und HUD.

const MAP_PATH: String = "res://data/maps/test_meadow.json"
## M1-Prototyp: Kapitel 2, damit der Größenwechsel überall (für Feenglanz)
## ausprobiert werden kann; an Feenringen ist er immer kostenlos.
const PROTOTYPE_CHAPTER: int = 2
## Genug Abstand für das Pferd (halbe Körperbreite), damit es an Zaunecken nicht hängen bleibt
const NAV_AGENT_RADIUS: float = 13.0

var builder: MapBuilder

@onready var _nav: NavigationRegion2D = $Nav
@onready var _ground: TileMapLayer = $Nav/Ground
@onready var _deco: Node2D = $Nav/Deco
@onready var _world: Node2D = $Nav/World
@onready var _fences: TileMapLayer = $Nav/World/Fences
@onready var _walls: StaticBody2D = $Nav/Walls
@onready var _klio: Klio = $Nav/World/Klio
@onready var _dog: SoulDog = $Nav/World/Dog
@onready var _horse: Horse = $Nav/World/Horse
@onready var _camera: PixelCamera = $Camera
@onready var _hud: CanvasLayer = $HUD


func _ready() -> void:
	GameState.heart_spring_chapter = maxi(GameState.heart_spring_chapter, PROTOTYPE_CHAPTER)
	TimeManager.running = false
	builder = MapBuilder.new(MAP_PATH)
	builder.build(_ground, _fences, _world, _deco, _walls)
	_klio.global_position = builder.spawns.get(&"klio", Vector2(320, 180))
	_dog.global_position = builder.spawns.get(&"dog", _klio.global_position + Vector2(-24, 8))
	_horse.global_position = builder.spawns.get(&"horse", _klio.global_position + Vector2(80, 0))
	_bake_navigation()
	_camera.set_bounds(Rect2i(Vector2i.ZERO, builder.pixel_size()))
	_camera.follow(_klio)
	_klio.camera_punch_requested.connect(_camera.punch)
	_hud.call(&"bind", _klio)


func _bake_navigation() -> void:
	var poly: NavigationPolygon = NavigationPolygon.new()
	poly.parsed_geometry_type = NavigationPolygon.PARSED_GEOMETRY_STATIC_COLLIDERS
	poly.parsed_collision_mask = PhysicsLayers.GROUND_MASK
	poly.agent_radius = NAV_AGENT_RADIUS
	var px: Vector2 = Vector2(builder.pixel_size())
	poly.add_outline(PackedVector2Array([Vector2.ZERO, Vector2(px.x, 0), px, Vector2(0, px.y)]))
	_nav.navigation_polygon = poly
	_nav.bake_navigation_polygon(false)
