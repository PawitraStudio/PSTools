import bpy

class PSSwitchRenderResolution(bpy.types.Operator):
    'Quick Switching Render Resolution'
    bl_idname = 'renderres.toggle'
    bl_label = 'Render Resolution Switching Toggle'

    def execute(self, context):
        rd = context.scene.render
        rs_x = rd.resolution_x
        rs_y = rd.resolution_y

        if rd.resolution_x == rs_x:
            rd.resolution_x = rs_y
            rd.resolution_y = rs_x
        else:
            rd.resolution_x = rs_x
            rd.resolution_y = rs_y
        return {'FINISHED'}