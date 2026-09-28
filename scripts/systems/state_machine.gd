class_name StateMachine
extends RefCounted
## Schlanke Zustandsmaschine: Zustände sind Namen mit optionalen Callbacks
## für Eintritt, Physik-Update und Austritt. Kein Knoten-Overhead, voll typisiert.

signal state_changed(from: StringName, to: StringName)

var current: StringName = &""
var time_in_state: float = 0.0

var _enter: Dictionary[StringName, Callable] = {}
var _update: Dictionary[StringName, Callable] = {}
var _exit: Dictionary[StringName, Callable] = {}


func add(state: StringName, on_update: Callable = Callable(), on_enter: Callable = Callable(),
		on_exit: Callable = Callable()) -> void:
	if on_update.is_valid():
		_update[state] = on_update
	if on_enter.is_valid():
		_enter[state] = on_enter
	if on_exit.is_valid():
		_exit[state] = on_exit


func has(state: StringName) -> bool:
	return _update.has(state) or _enter.has(state) or _exit.has(state)


func transition(to: StringName) -> void:
	if to == current:
		return
	var from: StringName = current
	if _exit.has(from):
		_exit[from].call()
	current = to
	time_in_state = 0.0
	if _enter.has(to):
		_enter[to].call()
	state_changed.emit(from, to)


func update(delta: float) -> void:
	time_in_state += delta
	if _update.has(current):
		_update[current].call(delta)


func is_in(state: StringName) -> bool:
	return current == state
