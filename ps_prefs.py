import bpy
import os
from bpy.types import AddonPreferences
from bpy.props import *
from . import addon_updater_ops


class PSToolsPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # addon updater preferences

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False,
        )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
        )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
        )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
        )
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
    prefs_tab_items = [
        ("GEN", "General Settings", "General settings for the addon."),
        ("UPDATE", "Addon Update Settings", "Settings for the addon updater.")]

    prefs_tab = bpy.props.EnumProperty(
        name="Options Set",
        items=prefs_tab_items
        )

    def draw(self, context):
        layout = self.layout
        preferences = context.user_preferences.addons[__package__].preferences

        row = layout.row()
        row.prop(self, "prefs_tab", expand=True)

        if preferences.prefs_tab == "GEN":
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

        if preferences.prefs_tab == "UPDATE":
            layout.row()
            addon_updater_ops.update_settings_ui(self, context)
