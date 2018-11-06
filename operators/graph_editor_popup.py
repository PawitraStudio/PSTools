import bpy

class GraphEditorPopup(bpy.types.Operator):
    'Enable Popup for Grapheditor'
    bl_idname = 'popup.grapheditor'
    bl_label = 'Graph Editor Show'

    def execute(self,context):
        # Call user prefs window
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')

        # Change area type
        area = bpy.context.window_manager.windows[-1].screen.areas[0]
        area.type = 'GRAPH_EDITOR'

        return {'FINISHED'}