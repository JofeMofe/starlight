class_name PhysicsLayers
extends RefCounted
## Kollisionsebenen (Namen in project.godot [layer_names]).
## Hohe Hindernisse (Bäume, Steine, Kartenrand) blockieren alle; niedrige
## (Zäune, Büsche, Wasser) überfliegt die Fee.

const SOLID_HIGH: int = 1 << 0
const SOLID_LOW: int = 1 << 1
const PLAYER: int = 1 << 2
const ANIMALS: int = 1 << 3
const INTERACT: int = 1 << 4

const GROUND_MASK: int = SOLID_HIGH | SOLID_LOW
const FLYING_MASK: int = SOLID_HIGH
