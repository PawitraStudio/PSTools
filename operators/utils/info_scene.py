import bpy
import os

def info_scene(self, context):
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    filename = os.path.splitext(filename)[0]
    layout = self.layout

    col = layout.column()
    if not context.blend_data.is_saved:
        col.label(text="File is not saved", icon='SCENE_DATA')
    elif context.blend_data.is_dirty == 1:
        col.label(text=" %s*" % (filename), icon='SCENE_DATA')
    else:
        col.label(text=" %s" % (filename), icon='SCENE_DATA')