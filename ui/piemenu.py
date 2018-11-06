import bpy
from bpy.types import Menu, Panel

class VIEW3D_PIE_pstools(Menu):
    bl_label = "PSTools Menu"

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator(
            "scene.simplify",
            text="Simplify!",
            icon="META_CUBE")
        pie.operator(
            "boundstextured.toggle",
            text="Quick Switch",
            icon="MATERIAL_DATA")
        pie.operator(
            "file.make_paths_relative",
            text="Make Relative",
            icon='LINK_AREA')
        pie.operator(
            "rotate.method",
            text="Orbit Style",
            icon='CAMERA_DATA')
        pie.operator(
            "VIEW3D_OT_view_selected",
            text="View Selected",
            icon='VIEWZOOM')
        pie.operator(
            "grid.toggle",
            text="Display Grid",
            icon='GRID')