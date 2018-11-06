import bpy
import os
from bpy import ops
from .utils.set_camera import setcamera

class PSOpenglTools(bpy.types.Operator):
    'Automatic OpenGL Render for most projects'
    bl_idname = 'opengl.toggle'
    bl_label = 'OpenglToggle'

    def execute(self, context):
        scene = context.scene
        render = scene.render
        space = context.space_data
        actions = bpy.data.actions

        setcamera(context)
        for action in actions:
            action.use_fake_user = 1
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        space.show_only_render = 1
        scene.frame_step = 1
        # scene.game_settings.material_mode = 'GLSL'
        # bpy.context.space_data.viewport_shade = 'MATERIAL'
        render.use_antialiasing = 0
        render.use_stamp = 1
        render.use_stamp_time = 0
        render.use_stamp_date = 0
        render.use_stamp_render_time = 0
        render.use_stamp_frame = 1
        render.use_stamp_scene = 0
        render.use_stamp_camera = 0
        render.use_stamp_lens = 1
        render.use_stamp_filename = 1
        render.use_stamp_note = 1
        render.stamp_font_size = 15
        render.stamp_background = (0, 0, 0, 0.25)
        render.stamp_foreground = (1, 1, 1, 1)
        # render.antialiasing_samples = '16'
        render.alpha_mode = 'SKY'
        render.use_raytrace = 0
        render.use_envmaps = 0
        render.use_sss = 0
        render.tile_x = 256
        render.tile_y = 256
        render.use_overwrite = 1
        render.use_file_extension = 1
        render.use_placeholder = 1
        #render.fps = 25
        render.resolution_percentage = 50
        # render.resolution_x = 1920
        # render.resolution_y = 1080
        render.use_simplify = 1
        render.simplify_subdivision = 0
        render.image_settings.file_format = 'FFMPEG'
        render.ffmpeg.format = 'MPEG4'
        render.ffmpeg.codec = 'H264'
        render.ffmpeg.audio_codec = 'AAC'
        # render.image_settings.compression = 100
        render.image_settings.color_mode = 'RGB'
        render.use_sequencer = 0
        render.use_freestyle = 0
        render.display_mode = 'NONE'

        parentdir = bpy.path.abspath(bpy.context.blend_data.filepath)
        parentdir = os.path.abspath(os.path.join(os.path.dirname(parentdir)))
        parentdir = os.path.basename(parentdir)
        parentdir = os.path.splitext(parentdir)[0]
        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        filename = os.path.splitext(filename)[0]

        render.stamp_note_text = filename
        scene.name = filename + "_scene"
        prefs = bpy.context.user_preferences.addons["PSTools"].preferences

        if filename:
            if filename.find('an') != -1:
                # filename = filename.split('an_')
                # filename = filename[1]
                render.filepath = os.path.join(
                    prefs.custom_path, filename + ".mp4") \
                    if prefs.use_custom_path else \
                    os.path.join(
                        "//../../render/playblast/", filename + ".mp4")
            else:
                render.filepath = os.path.join(
                    prefs.custom_path, filename + ".mp4") \
                    if prefs.use_custom_path else \
                    os.path.join(
                        "//../../render/playblast/", filename + ".mp4")

        scene.render.use_lock_interface = True

        bpy.ops.wm.console_toggle()
        os.system('cls')
        print ('Creating Boomsmash File ...')
        bpy.ops.render.opengl(
            animation = True,
            sequencer = False)
        print('Done')
        if prefs.use_autoplay is True:
            bpy.ops.render.play_rendered_anim()
        bpy.ops.wm.console_toggle()

        self.blendpath = bpy.path.abspath(context.blend_data.filepath)
        bpy.ops.wm.open_mainfile(filepath=self.blendpath)

        return {'FINISHED'}