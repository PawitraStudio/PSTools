import bpy

class PSSetFrames(bpy.types.Operator):
    'Use current scenes frame start and end for all scenes available'
    bl_idname = 'setframes.toggle'
    bl_label = 'Set Frames'

    def execute(self, context):
        sf = bpy.context.scene.frame_start
        ef = bpy.context.scene.frame_end

        for n in bpy.data.scenes:
            n.frame_start = sf
            n.frame_end = ef

        return {'FINISHED'}