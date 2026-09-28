extends SceneTree
## GDScript-Warnungs-Scanner. Godot druckt Analyzer-Warnungen nur im
## Debug-Modus (-d) und ohne Dateinamen; daher wird jedes Projektskript
## einzeln ohne Cache neu geladen und vorher sein Pfad markiert.
## Auswertung: tools/lint/lint_gdscript.py

const ROOTS: PackedStringArray = ["res://scripts", "res://scenes", "res://tests", "res://tools"]


func _init() -> void:
	# Autoload-Bezeichner existieren erst nach dem ersten Frame.
	process_frame.connect(_run, CONNECT_ONE_SHOT)


func _run() -> void:
	var files: PackedStringArray = []
	for base_dir: String in ROOTS:
		_collect(base_dir, files)
	for path: String in files:
		print("LINT_FILE ", path)
		ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_IGNORE)
	print("LINT_DONE ", files.size())
	quit(0)


func _collect(dir_path: String, out: PackedStringArray) -> void:
	var dir: DirAccess = DirAccess.open(dir_path)
	if dir == null:
		return
	for sub: String in dir.get_directories():
		_collect(dir_path.path_join(sub), out)
	for file: String in dir.get_files():
		# Der Scanner selbst darf sich nicht neu laden (Absturz der VM).
		if file.get_extension() == "gd" and dir_path.path_join(file) != get_script().resource_path:
			out.append(dir_path.path_join(file))
