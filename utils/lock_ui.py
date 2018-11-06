import bpy
from bpy.types import Menu, Panel
from bpy import context
# Below code was copied from here
# https://gist.github.com/Fweeb/bb61c15139bff338cb17
def lock_ui(self, context):
    layout = self.layout

    layout.prop(
        context.space_data.region_3d,
        'lock_rotation',
        text='Lock View Rotation')