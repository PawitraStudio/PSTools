import bpy
import os

class KSEditSetup(bpy.types.Operator):
    'Auto Setup for Rendering Edit Sequence per unit in Kidsong Project'
    bl_idname = 'set.ksedit'
    bl_label = 'SetKSEdit'

    @classmethod
    def poll(cls,context):
        return bpy.data.filepath != ""\
            and bpy.context.scene.render.use_sequencer == 1

    def execute(self, context):
        scenes = bpy.data.scenes
        scene = bpy.context.scene
        render = scene.render

        orig_seqs = scenes[0].sequence_editor.sequences
        strip_text = [strip for strip in orig_seqs if strip.type == 'TEXT']
        for strip in strip_text:
            strip.mute = True

        scene.view_settings.exposure = 0
        scene.view_settings.gamma = 1
        render.use_compositing = False
        render.resolution_percentage = 100
        render.image_settings.file_format = 'FFMPEG'
        render.image_settings.color_mode = 'RGB'
        render.ffmpeg.format = 'QUICKTIME'
        render.ffmpeg.codec = 'H264'
        render.ffmpeg.constant_rate_factor = 'HIGH'
        render.ffmpeg.audio_codec = 'AAC'
        if bpy.app.version >= (2,79,5):
            render.ffmpeg.ffmpeg_preset = 'GOOD'
        else :
            render.ffmpeg.ffmpeg_preset = 'MEDIUM'

        bpy.ops.wm.console_toggle()
        os.system('cls')
        print ('Creating Boomsmash File ...')
        bpy.ops.render.opengl(animation=True, sequencer=True)
        print ('Done')

        return {'FINISHED'}