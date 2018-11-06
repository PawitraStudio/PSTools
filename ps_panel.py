import bpy
import os
from bpy.types import Menu, Panel
from bpy import context
from . import addon_updater_ops











def register():
    # bpy.utils.register_module(__name__)
    bpy.types.RENDER_PT_dimensions.append(PSSwitchRenderResolution)
    bpy.types.INFO_HT_header.prepend(PSFileFunction)
    bpy.types.NODE_HT_header.append(setpath)
    bpy.types.VIEW3D_PT_view3d_properties.append(lock_ui)
    bpy.types.SEQUENCER_HT_header.append(KSEditSetup)

def unregister():
    # bpy.utils.unregister_module(__name__)
    bpy.types.RENDER_PT_dimensions.remove(PSSwitchRenderResolution)
    bpy.types.INFO_HT_header.remove(PSFileFunction)
    bpy.types.NODE_HT_header.remove(setpath)
    bpy.types.VIEW3D_PT_view3d_properties.remove(lock_ui)
    bpy.types.SEQUENCER_HT_header.remove(KSEditSetup)

if __name__ == "__main__":
    register()
