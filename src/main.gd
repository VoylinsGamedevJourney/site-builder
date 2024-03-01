class_name Main extends Control

static var instance: Main

# Keep same order as panels in TABS
enum SCREENS { STARTUP, SITE_SETTINGS, SITE_OVERVIEW }


func _ready():
	# Instance setting
	if instance != null:
		printerr("Startup instance is not null!")
		return
	instance = self
	print_rich("[b]--==  Starting site builder  ==--")
	
	# TODO: See if program was opened with a directory or not. 
	#       If yes, skip startup
	switch_screen(SCREENS.STARTUP)
	Startup.load_list()


static func switch_screen(tab_id: SCREENS) -> void:
	instance._switch_screen(tab_id)


func _switch_screen(tab_id: SCREENS) -> void:
	$Tabs.current_tab = tab_id
