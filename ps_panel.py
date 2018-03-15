import bpy
import os
from bpy.types import Menu, Panel
from bpy import context
from . import addon_updater_ops

# Below code was copied from here
# https://gist.github.com/Fweeb/bb61c15139bff338cb17


def setpath(self, context):
    layout = self.layout

    col = layout.column()
    row = col.row(align=True)

    row.operator(
        "set.renderpath",
        text="Set Path",
        icon="FILE_FOLDER")


def lock_ui(self, context):
    layout = self.layout

    layout.prop(
        context.space_data.region_3d,
        'lock_rotation',
        text='Lock View Rotation')


def PSSwitchRenderResolution(self, context):
    layout = self.layout
    col = layout.column(align=True)
    col.operator(
        "renderres.toggle",
        text='Switch Resolution',
        icon='FILE_REFRESH')


def PSFileFunction(self, context):
    layout = self.layout

    col = layout.column()
    row = col.row(align=True)

    row.alignment = 'CENTER'
    row.operator(
        "wm.window_fullscreen_toggle",
        icon="FULLSCREEN_ENTER",
        text="")
    row.operator(
        "wm.quit_blender",
        icon="QUIT",
        text="")
    row.operator(
        "ps.save_file",
        icon="FILE_TICK",
        text="")
    row.operator(
        "ps.save_progress",
        icon="OPEN_RECENT",
        text="")
    row.operator(
        "ps.save_file_increment",
        icon="ZOOMIN",
        text="")
    row.operator(
        "wm.save_as_mainfile",
        icon="SAVE_AS",
        text="")
    row.operator(
        "wm.open_mainfile",
        icon="FILE_FOLDER",
        text="")
    row.operator(
        "wm.link",
        icon="LINK_BLEND",
        text="")
    row.operator(
        "wm.append",
        icon="APPEND_BLEND",
        text="")
    row.operator(
        "shots.relink",
        icon="LIBRARY_DATA_DIRECT",
        text="")


def PSOpenglrender(self, context):
    layout = self.layout

    col = layout.column()
    row = col.row(align=True)

    row.operator(
        "opengl.toggle",
        text='Boomsmash',
        icon="CLIP")


class PSTools(bpy.types.Panel):
    bl_label = "PSTools"
    bl_category = "PSTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Setup Tools ")

        col.operator(
            "boundstextured.toggle",
            text="Quick Switch",
            icon="MATERIAL_DATA")
        col.operator(
            "setframes.toggle",
            text="Set Frames",
            icon="TIME")
        col.operator(
            "file.make_paths_relative",
            text="Make Relative",
            icon='LINK_AREA')
        col.operator(
            "file.find_missing_files",
            text="Find Missing",
            icon='ZOOM_ALL')
        col.operator(
            "render.render",
            text="Render",
            icon='RENDER_STILL')
        col.operator(
            "opengl.toggle",
            text="Boomsmash",
            icon="CLIP")
        col.operator(
            "set.renderpath",
            text="Set Path",
            icon="FILE_FOLDER")
        col.operator(
            "scene.simplify",
            text="Simplify",
            icon="META_CUBE")
        
        col.separator()

        view = context.scene.render
        scene = context.scene
        space = context.space_data

        row = layout.row()
        row.prop(view, "use_simplify", text="Simplify")
        sub = row.column()
        sub.active = view.use_simplify
        sub.prop(view, "simplify_subdivision", text="Level")
        row.separator()

        col = layout.column()
        col.prop(space, "show_only_render")
        col.prop(space, "lock_camera")
        col.label(text="Adjust Frame")
        row = layout.row()
        row.prop(context.scene, "frame_start", text="in")
        row.prop(context.scene, "frame_end", text="out")
        row.separator()


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


class PSToolsUpdaterPanel(bpy.types.Panel):
    """Panel to demo popup notice and ignoring functionality"""
    bl_label = "Updater Panel"
    bl_idname = "OBJECT_PT_update"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = "PSTools"

    def draw(self, context):
        layout = self.layout
        addon_updater_ops.check_for_update_background(context)

        layout.label("Pawitra Tools Updater Addon")
        layout.label("")

        layout.label("If an update is ready,")
        layout.label("popup triggered by opening")
        layout.label("this panel & plus a box ui")

        if addon_updater_ops.updater.update_ready is True:
            layout.label("Custom update message", icon="INFO")
        layout.label("")

        addon_updater_ops.update_notice_box_ui(self, context)


def register():
    bpy.types.RENDER_PT_dimensions.append(PSSwitchRenderResolution)
    bpy.types.INFO_HT_header.prepend(PSFileFunction)
    bpy.types.NODE_HT_header.append(setpath)
    bpy.types.VIEW3D_PT_view3d_properties.append(lock_ui)


def unregister():
    bpy.types.RENDER_PT_dimensions.remove(PSSwitchRenderResolution)
    bpy.types.INFO_HT_header.remove(PSFileFunction)
    bpy.types.NODE_HT_header.remove(setpath)
    bpy.types.VIEW3D_PT_view3d_properties.remove(lock_ui)


if __name__ == "__main__":
    register()
