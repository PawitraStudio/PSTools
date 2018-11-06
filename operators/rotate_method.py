import bpy

class PSRotateMethod(bpy.types.Operator):
    bl_idname = "rotate.method"
    bl_label = "Rotate Method"

    def execute(self, context):
        userpref = context.user_preferences
        inputs = userpref.inputs

        if inputs.view_rotate_method == 'TURNTABLE':
            inputs.view_rotate_method = 'TRACKBALL'
        else:
            inputs.view_rotate_method = 'TURNTABLE'
        return{'FINISHED'}