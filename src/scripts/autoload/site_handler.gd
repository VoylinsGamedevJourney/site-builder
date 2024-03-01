extends Node

const PATH_SITE_INFO := "%s/site_info.json"

const DEFAULT_FOLDERS: PackedStringArray = [
	"_site", "assets", "pages", "toolbox", "pages", "posts",
	"assets/thumbs",
	"toolbox/templates",
	"toolbox/blocks" ]
const DEFAULT_FILES: PackedStringArray = [
	"assets/style_001.css",
	"toolbox/blocks/footer.html",
	"toolbox/blocks/head.html",
	"toolbox/templates/page.html",
	"toolbox/templates/post.html"]


var dir: String
var site_title: String
var site_description: String
var site_url: String
var site_tags: PackedStringArray
var site_categories: PackedStringArray
var site_author: String


func load_site(dir_path: String) -> void:
	dir = dir_path
	
	# Check if site_json exists
	
	
	# Check if all default folders exist else create folder
	for folder: String in DEFAULT_FOLDERS:
		var folder_path := "%s/%s" % [dir, folder]
		if !DirAccess.dir_exists_absolute(folder_path):
			DirAccess.make_dir_absolute(folder_path)
	
	# Check if all default files exist else create file
	for file_entry: String in DEFAULT_FILES:
		var default_file_path: String = "res://default_files/%s" % file_entry.split('/')[-1]
		var site_file_path: String = "%s/%s" % [dir, file_entry]
		if !FileAccess.file_exists(site_file_path):
			var file := FileAccess.open(default_file_path, FileAccess.READ)
			var default_data := file.get_as_text()
			file.close()
			file.open(site_file_path, FileAccess.WRITE)
			file.store_string(default_data)
