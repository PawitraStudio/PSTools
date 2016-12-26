bl_info = {
    "name": "Pawitra Studio Tools",
    "description": "A series of tools that being used in Pawitra Studio",
    "author": "Aditia A. Pratama",
    "version": (1, 0, 1),
    "blender": (2, 78),
    "location": "Tools Panel",
    "warning": '',  # used for warning icon and text in addons panel
    "wiki_url": "http://gihub.com/PawitraStudio/PSTools",
    "tracker_url": "",
    "category": "3D View"}

import sys, os
pstoolsDirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', pstoolsDirname))

if "bpy" in locals():
    import imp
    imp.reload(ps_operators)
    imp.reload(ps_panel)
    imp.reload(addon_updater_ops)

    print("Reloaded PSTools")

else:
    from . import ps_operators, ps_panel, addon_updater_ops

    print("Imported PSTools")

import ps_operators
import ps_panel

import bpy
from bpy.types import AddonPreferences

class PSToolsUpdaterPanel(bpy.types.Panel):
	"""Panel to demo popup notice and ignoring functionality"""
	bl_label = "Updater Panel"
	bl_idname = "OBJECT_PT_hello"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_context = "objectmode"
	bl_category = "PSTools"

	def draw(self, context):
		layout = self.layout

		# Call to check for update in background
		# note: built-in checks ensure it runs at most once
		# and will run in the background thread, not blocking
		# or hanging blender
		# Internal also checks to see if auto-check enabeld
		# and if the time interval has passed
		addon_updater_ops.check_for_update_background(context)


		layout.label("Pawitra Tools Updater Addon")
		layout.label("")

		layout.label("If an update is ready,")
		layout.label("popup triggered by opening")
		layout.label("this panel & plus a box ui")

		# could also use your own custom drawing
		# based on shared variables
		if addon_updater_ops.updater.update_ready == True:
			layout.label("Custom update message", icon="INFO")
		layout.label("")

		# call built-in function with draw code/checks
		addon_updater_ops.update_notice_box_ui(self, context)


# demo bare-bones preferences
class PSToolsPreferences(bpy.types.AddonPreferences):
	bl_idname = __package__

	# addon updater preferences

	auto_check_update = bpy.props.BoolProperty(
		name = "Auto-check for Update",
		description = "If enabled, auto-check for updates using an interval",
		default = False,
		)

	updater_intrval_months = bpy.props.IntProperty(
		name='Months',
		description = "Number of months between checking for updates",
		default=0,
		min=0
		)
	updater_intrval_days = bpy.props.IntProperty(
		name='Days',
		description = "Number of days between checking for updates",
		default=7,
		min=0,
		)
	updater_intrval_hours = bpy.props.IntProperty(
		name='Hours',
		description = "Number of hours between checking for updates",
		default=0,
		min=0,
		max=23
		)
	updater_intrval_minutes = bpy.props.IntProperty(
		name='Minutes',
		description = "Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59
		)

	def draw(self, context):

		layout = self.layout

		# updater draw function
		addon_updater_ops.update_settings_ui(self,context)

addon_keymaps = []

def register():
   ps_operators.register()
   ps_panel.register()
   addon_updater_ops.register(bl_info)
   bpy.utils.register_class(PSToolsUpdaterPanel)
   bpy.utils.register_class(PSToolsPreferences)

   addon_keymaps.clear()
   kc = bpy.context.window_manager.keyconfigs.addon

   if kc:
    km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'E', 'PRESS', shift=True)
    kmi.properties.name = 'VIEW3D_PIE_pstools'

    addon_keymaps.append(km)

def unregister():
    ps_operators.unregister()
    ps_panel.unregister()
    addon_updater_ops.unregister()
    bpy.utils.unregister_class(PSToolsUpdaterPanel)
    bpy.utils.unregister_class(PSToolsPreferences)

    # remove the add-on keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
