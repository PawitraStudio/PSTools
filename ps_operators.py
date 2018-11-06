import os
import bpy
import blend_render_info
from bpy import ops
from bpy.props import BoolProperty
from bpy.types import Operator, Panel
from . import ps_prefs

# TODO : need to add presets for any project
# class PSScenesRender(bpy.types.Operator):
#     'Adjust Render Reseolution for all scenes'
#     bl_idname = 'scn.renderres'
#     bl_label = 'Scene Render Resolution'



def register():
    bpy.types.INFO_HT_header.prepend(info_scene)
    bpy.types.Scene.RNSeparator = bpy.props.StringProperty(
         name="Separator",
         default="_",
         description="The bit between the base name and incremented number")

def unregister():
    del bpy.types.Scene.RNSeparator
    bpy.types.INFO_HT_header.remove(info_scene)

if __name__ == "__main__":
    register()
