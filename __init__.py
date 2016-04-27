bl_info = {
    "name": "Pawitra Studio Tools",
    "description": "A series of tools that being used in Pawitra Studio",
    "author": "Aditia A. Pratama",
    "version": (0, 1, 0),
    "blender": (2, 77),
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

    print("Reloaded PSTools")

else:
    from . import ps_operators, ps_panel

    print("Imported PSTools")

import ps_operators
import ps_panel

import bpy
from bpy.types import AddonPreferences

####

addon_keymaps = []

def register():
   ps_operators.register()
   ps_panel.register()

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

    # remove the add-on keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
