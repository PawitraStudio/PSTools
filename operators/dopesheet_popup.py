import bpy

class DopesheetPopup(bpy.types.Operator):
    'Enable Popup for Dopesheet'
    bl_idname = 'popup.dopesheet'
    bl_label = 'Graph Editor Show'

    def execute(self,context):
        # Call user prefs window
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')

        # Change area type
        area = bpy.context.window_manager.windows[-1].screen.areas[0]
        area.type = 'DOPESHEET_EDITOR'

        return {'FINISHED'}