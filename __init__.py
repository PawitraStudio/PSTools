import bpy
from . import ps_prefs
from . import ps_operators
from . import ps_panel
from . import addon_updater_ops

bl_info = {
    "name": "Pawitra Studio Tools",
    "description": "A series of tools that being used in Pawitra Studio",
    "author": "Aditia A. Pratama",
    "version": (1, 1, 4),
    "blender": (2, 79),
    "location": "Tools Panel",
    "warning": '',  # used for warning icon and text in addons panel
    "wiki_url": "http://gihub.com/PawitraStudio/PSTools",
    "tracker_url": "",
    "category": "3D View"}

addon_keymaps = []


def register():
    bpy.utils.register_module(__name__)
    # addon_updater_ops.register(bl_info)
    ps_operators.register()
    ps_panel.register()
    addon_keymaps.clear()
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'E', 'PRESS', shift=True)
        kmi.properties.name = 'VIEW3D_PIE_pstools'
    addon_keymaps.append((km, kmi))


def unregister():
    # remove the add-on keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    ps_panel.unregister()
    ps_operators.unregister()
    # addon_updater_ops.unregister()
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
