class_name MovementConfig
extends Resource
## Alle Bewegungs- und Gefühlswerte für Klio, Hund und Pferd (§6, §7.1, §7.2).
## Instanz: res://data/config/movement.tres. Einheiten: Pixel, Sekunden.

@export_group("Klio – Menschengröße")
@export var human_speed: float = 82.0
## Beschleunigung: 0 -> Höchsttempo in ~0,11 s (direkt, aber nicht ruckartig)
@export var human_accel: float = 760.0
## Abbremsen: Höchsttempo -> 0 in ~0,08 s (kein Rutschen)
@export var human_friction: float = 1050.0

@export_group("Klio – Feengröße")
@export var fairy_speed: float = 70.0
@export var fairy_fly_speed: float = 98.0
## Die Fee schwebt: weicher an- und auslaufen als in Menschengröße
@export var fairy_accel: float = 430.0
@export var fairy_friction: float = 520.0
@export var fly_height: float = 10.0
@export var hover_amplitude: float = 1.5
@export var hover_frequency: float = 2.2
@export var flight_energy_max: float = 100.0
@export var flight_drain_per_second: float = 32.0
@export var flight_regen_per_second: float = 55.0
@export var flight_regen_delay: float = 0.35

@export_group("Größenwechsel")
@export var transform_duration: float = 0.4
@export var transform_swap_time: float = 0.2
## Feenglanz-Kosten außerhalb von Feenringen (ab Kapitel 2), ab Kapitel 4 kostenlos
@export var transform_glow_cost: float = 5.0
@export var free_transform_chapter: int = 4
@export var anywhere_transform_chapter: int = 2

@export_group("Hund")
@export var dog_follow_distance: float = 30.0
@export var dog_run_distance: float = 90.0
@export var dog_walk_speed: float = 62.0
@export var dog_run_speed: float = 128.0
@export var dog_accel: float = 600.0
## Geritten (Fee auf dem Rücken): schneller als die fliegende Fee
@export var dog_ridden_speed: float = 150.0
@export var dog_ridden_accel: float = 820.0
@export var dog_sit_delay: float = 2.5

@export_group("Pferd")
@export var horse_walk_speed: float = 52.0
@export var horse_trot_speed: float = 108.0
@export var horse_canter_speed: float = 172.0
## Tempoänderung in px/s²: bewusst träge, damit sich das Pferd schwer anfühlt
@export var horse_accel: float = 170.0
@export var horse_decel: float = 230.0
## Wendigkeit in Grad/s je Gangart (Schritt, Trab, Galopp) -> Wendekreis
@export var horse_turn_rates: PackedFloat32Array = PackedFloat32Array([420.0, 230.0, 150.0])
@export var horse_jump_duration: float = 0.46
@export var horse_jump_height: float = 11.0
@export var horse_come_speed: float = 95.0
