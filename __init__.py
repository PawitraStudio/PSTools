import bpy
import blend_render_info
from bpy import ops
from bpy.props import BoolProperty, IntProperty, EnumProperty, StringProperty
from bpy.types import Operator, Panel

# Rregister
import traceback
from .operators import *
from .operators.EnglishTimeSongOPS import *
from .ui import panel, piemenu
from .utils.lock_ui import lock_ui
from .utils.switch_render_resolution import PSSwitchRenderResolution
from .utils.file_function import PSFileFunction
# from . import addon_updater_ops

#Load and reload submodules
from .utils import addon_auto_imports
modules = addon_auto_imports.setup_addon_modules(__path__, __name__, ignore_packages=[".utils"], ignore_modules=["addon_updater"])

bl_info = {
    "name": "PSTools",
    "description": "Pawitra Studio Script Toolset ",
    "author": "Aditia A. Pratama",
    "version": (2, 0, 0),
    "blender": (2, 79),
    "location": "Tools Panel",
    "warning": '',  # used for warning icon and text in addons panel
    "wiki_url": "http://gihub.com/PawitraStudio/PSTools",
    "tracker_url": "",
    "category": "3D View"}

class PSToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    use_custom_path = bpy.props.BoolProperty(
        name="Use Custom Path",
        description="Enable to use custom path folder for Playblast file",
        default=False
        )
    use_autoplay = bpy.props.BoolProperty(
        name="Use Autoplay",
        description="Enable to play video automatically after render ",
        default=False
        )
    custom_path = bpy.props.StringProperty(
        name="Custom Path",
        description="""Custom path for Playblast files.""",
        subtype='DIR_PATH'
        )

    def draw(self, context):
        layout = self.layout
        preferences = context.user_preferences.addons[__package__].preferences

        row = layout.row()
        # row.prop(self, "prefs_tab", expand=True)

        # if preferences.prefs_tab == "GEN":
        layout.row()
        layout = self.layout
        box = layout.box()
        box.label("OpenGl/Playblast Settings :")

        row = box.row()
        row.prop(self, 'use_autoplay')
        row.prop(self, 'use_custom_path')

        col = box.column()
        row = col.row()
        row.label("Custom Playblast Path:")
        row.active = self.use_custom_path
        row.prop(self, "custom_path", text="")


addon_keymaps = []

def register():
    try:
        bpy.utils.register_module(__name__)
    except:
        traceback.print_exc()

    bpy.types.INFO_HT_header.prepend(info_scene)
    bpy.types.Scene.RNSeparator = bpy.props.StringProperty(
         name="Separator",
         default="_",
         description="The bit between the base name and incremented number")

    bpy.types.RENDER_PT_dimensions.append(PSSwitchRenderResolution)
    bpy.types.INFO_HT_header.prepend(PSFileFunction)
    bpy.types.VIEW3D_PT_view3d_properties.append(lock_ui)

    addon_keymaps.clear()
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'E', 'PRESS', shift=True)
        kmi.properties.name = 'VIEW3D_PIE_pstools'
    addon_keymaps.append((km, kmi))

    print("Registered {} with {} modules".format(bl_info["name"], len(
        modules)))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.types.RENDER_PT_dimensions.remove(PSSwitchRenderResolution)
    bpy.types.INFO_HT_header.remove(PSFileFunction)
    bpy.types.VIEW3D_PT_view3d_properties.remove(lock_ui)

    del bpy.types.Scene.RNSeparator
    bpy.types.INFO_HT_header.remove(info_scene)

    try:
        bpy.utils.unregister_module(__name__)
    except:
        traceback.print_exc()

    print("Unregistered {}".format(bl_info["name"]))

# if __name__ == "__main__":
#     register()
