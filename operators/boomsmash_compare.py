import bpy
import os
from .utils.set_camera import setcamera

class PSCompareBoomsmash(bpy.types.Operator):
    'Automatic Comparing current shot boomsmash with reference in VSE'
    bl_idname = 'boomsmash.compare'
    bl_label = 'Compare Boomsmash'

    @classmethod
    def poll(cls, context):
        return bpy.data.filepath != ""

    def execute(self, context):
        scenes = bpy.data.scenes
        scene = bpy.context.scene
        filename = bpy.path.display_name_from_filepath(bpy.data.filepath)
        frame_start = scene.frame_preview_start

        #Ensure current scene name is equal to filename
        #bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        scenes[0].name = filename

        actions = bpy.data.actions
        for action in actions:
            action.use_fake_user = 1

        prefs = bpy.context.user_preferences.addons[__package__].preferences

        if filename:
            if filename.find('an') != -1:
                scene.render.filepath = os.path.join(
                    prefs.custom_path, filename + ".mp4") \
                    if prefs.use_custom_path else \
                    os.path.join(
                        "//", filename + ".mp4")
            else:
                scene.render.filepath = os.path.join(
                    prefs.custom_path, filename + ".mp4") \
                    if prefs.use_custom_path else \
                    os.path.join(
                        "//", filename + ".mp4")

        #store clip path and reverse the order (movie is always in 2nd channel)
        orig_seqs= scenes[0].sequence_editor.sequences
        clip_path = [clip for clip in orig_seqs if clip.type == 'MOVIE']
        for clip in clip_path:
            clip_path = bpy.path.abspath(clip.filepath)

        all_seqs = [seq for seq in orig_seqs]
        sound_seqs = [sound for sound in orig_seqs if sound.type == 'SOUND']

        for sound in sound_seqs:
            orig_seqs.remove(sound)
        for seq in all_seqs:
            if seq.type == 'MOVIE':
                seq.channel = 2
                movpath = seq.filepath
                orig_seqs.new_sound(
                            'sound',
                            bpy.path.abspath(movpath),
                            1, frame_start)

        #create new scene copy
        edit_name='edit_'+filename
        if len(scenes) == 1:
            for scn in scenes:
                if scn.name.startswith('edit_') == False:
                    bpy.ops.scene.new(type='EMPTY')
                    scenes[1].name = edit_name

                    mainScreen = bpy.context.screen
                    mainScreen.scene = scenes[1]

            for scn in scenes:
                if scn.name.startswith('edit_') == True:
                    scn.render.use_compositing = False
                    scn.render.use_sequencer = True
                    scn.sequence_editor_create()
                    # scene render settings
                    scn.render.use_stamp = 1
                    scn.render.use_stamp_time = 0
                    scn.render.use_stamp_date = 0
                    scn.render.use_stamp_render_time = 0
                    scn.render.use_stamp_frame = 1
                    scn.render.use_stamp_scene = 0
                    scn.render.use_stamp_camera = 0
                    scn.render.use_stamp_lens = 0
                    scn.render.use_stamp_filename = 0
                    scn.render.use_stamp_note = 0
                    scn.render.stamp_font_size = 15
                    scn.render.stamp_background = (0, 0, 0, 0.25)
                    scn.render.stamp_foreground = (1, 1, 1, 1)
                    scn.render.resolution_x = 1920*2
                    scn.render.resolution_percentage = 25
                    # scn.render.filepath = '//'
                    scn.render.image_settings.file_format = 'FFMPEG'
                    scn.render.ffmpeg.format = "MPEG4"
                    scn.render.ffmpeg.codec = "H264"
                    # scn.render.ffmpeg.gopsize = 1
                    # scn.render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'
                    # scn.render.ffmpeg.use_max_b_frames = True
                    # scn.render.ffmpeg.max_b_frames = 0
                    scn.render.ffmpeg.audio_codec = 'AAC'
                    scn.render.use_lock_interface = True
                    seqs = scn.sequence_editor.sequences

                    if len(seqs) == 0:
                        seqs.new_scene(
                            filename,
                            scenes[0],
                            1, frame_start)
                        seqs.new_effect(
                            'transform_01',
                            'TRANSFORM',
                            2, frame_start,
                            seq1=seqs[0])

                    scn.render.sequencer_gl_preview = 'MATERIAL'
                    if len(seqs)==2:
                        seqs.new_movie(
                            'mov_'+filename,
                            bpy.path.abspath(clip_path),
                            3, frame_start)
                        seqs.new_sound(
                            'aud_'+filename,
                            bpy.path.abspath(clip_path),
                            4, frame_start)
                        seqs.new_effect(
                            'transform_02',
                            'TRANSFORM',
                            5, frame_start,
                            seq1=seqs[2])

                        for seq in seqs:
                            if seq.channel == 2:
                                seq.select = True
                                seq.scale_start_x = 0.5
                                seq.translate_start_x = -25
                            elif seq.channel == 5:
                                seq.select = True
                                seq.scale_start_x = 0.5
                                seq.translate_start_x = 25
                                seq.blend_type = 'ALPHA_OVER'

                    bpy.ops.wm.console_toggle()
                    os.system('cls')
                    print ('Creating Boomsmash File ...')
                    bpy.ops.render.opengl(animation=True, sequencer=True)
                    print ('Done')
                    if prefs.use_autoplay is True:
                        bpy.ops.render.play_rendered_anim()
                    #bpy.ops.wm.path_open(filepath=scn.render.filepath)
                    # bpy.ops.render.play_rendered_anim()
                    bpy.ops.wm.console_toggle()

                    self.blendpath = bpy.path.abspath(context.blend_data.filepath)
                    bpy.ops.wm.open_mainfile(filepath=self.blendpath)

        return {'FINISHED'}