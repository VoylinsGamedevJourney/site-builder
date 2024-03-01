class_name Startup extends PanelContainer
# TODO: Check if sites_list doesn't contain duplicates

static var instance: Startup


const PATH := "user://sites_list"


func _ready():
	## Instance setting
	if instance != null:
		printerr("Startup instance is not null!")
		return
	instance = self


func add_new_site(dir: String) -> void:
	if !FileAccess.file_exists(PATH):
		print("Creating sites_list ...")
		var file := FileAccess.open(PATH, FileAccess.WRITE)
		file.store_line(dir)
		file.close()
		return
	print("Adding '%s' to sites list and sorting ..." % dir)
	var file := FileAccess.open(PATH, FileAccess.READ)
	var data: PackedStringArray = file.get_as_text().split("\n")
	
	data.append(dir)
	data.sort()
	
	var new_data: PackedStringArray
	for line: String in data:
		if line == "":
			continue
		if line in new_data:
			continue
		new_data.append(line)
	
	file = FileAccess.open(PATH, FileAccess.WRITE)
	for line: String in new_data:
		file.store_line(line)
	file.close()


static func load_list() -> void:
	instance._load_list()


func _load_list() -> void:
	## Loading the list of all previously worked on projects
	if !FileAccess.file_exists(PATH):
		print("No sites list found!")
		return
	print("Fetching sites list ...")
	var file := FileAccess.open(PATH, FileAccess.READ)
	var button := Button.new()
	for dir: String in file.get_as_text().split('\n'):
		if dir == "": break # EOF
		if !DirAccess.dir_exists_absolute(dir):
			printerr("Previously saved site location doesn't exist (anymore)!")
			continue
		if !FileAccess.file_exists("%s/site_info.json" % dir):
			printerr("Previously saved site location doesn't have site_info.json!")
			print("%s/site_info.json" % dir)
			continue
		var site_button: Button = button.duplicate()
		site_button.text = dir.split('/')[-1]
		site_button.pressed.connect(site_button_pressed.bind(dir))
		%SitesList.add_child(site_button)


func site_button_pressed(path: String) -> void:
	Main.switch_screen(Main.SCREENS.SITE_OVERVIEW)


func _on_new_site_button_pressed():
	var dialog := FileDialog.new()
	dialog.access = FileDialog.ACCESS_FILESYSTEM
	dialog.file_mode = FileDialog.FILE_MODE_OPEN_DIR
	dialog.show_hidden_files = true
	dialog.use_native_dialog = true
	dialog.dir_selected.connect(func(dir: String):
		add_new_site(dir)
		site_button_pressed(dir)
		Main.switch_screen(Main.SCREENS.SITE_SETTINGS))
	add_child(dialog)
	dialog.popup_centered()


func _on_open_site_button_pressed():
	var dialog := FileDialog.new()
	dialog.access = FileDialog.ACCESS_FILESYSTEM
	dialog.file_mode = FileDialog.FILE_MODE_OPEN_DIR
	dialog.show_hidden_files = true
	dialog.use_native_dialog = true
	dialog.dir_selected.connect(func(dir: String):
		if !FileAccess.file_exists("%s/site_info.json" % dir):
			print("Can't open website as no site_info was found in selected folder!")
			return
		print(dir)
		add_new_site(dir)
		site_button_pressed(dir)
		Main.switch_screen(Main.SCREENS.SITE_OVERVIEW))
	add_child(dialog)
	dialog.popup_centered()
