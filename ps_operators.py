import os
import bpy
import blend_render_info
from bpy import ops
from bpy.props import BoolProperty
from bpy.types import Operator, Panel

# TODO : need to add presets for any project
#TODO add user preferences for output opengl render

def setcamera(context):
    view3d = bpy.context.space_data.region_3d

    for ob in bpy.context.scene.objects:
        if view3d.view_perspective != 'CAMERA':
            bpy.ops.view3d.viewnumpad(type='CAMERA')
    return setcamera

class PSRelinkShots(bpy.types.Operator):
    'Auto Relink Shots File'
    bl_idname='shots.relink'
    bl_label='ShotsRelink'

    @classmethod
    def poll(cls, context):
        return bpy.data.filepath != "" and bpy.data.filepath.startswith("lg_")

    def execute(self, context):
        objects = bpy.data.objects
        scene = bpy.context.scene

        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        filename = os.path.splitext(filename)[0]
        filename = filename.split('_light')
        filename = bpy.path.ensure_ext(filename[0], ext = '.blend')

        blendpath = bpy.path.abspath (bpy.context.blend_data.filepath)
        blenddir, blendfile= os.path.split(blendpath)
        filepath = os.path.join(blenddir + '/' + filename)

        for obj in objects:
            if obj.get is not None and obj.type != 'LAMP':
            #    obj.select = True
            #else :
            #    obj.select = False
            #bpy.ops.object.delete()
                bpy.data.objects.remove(obj, do_unlink=True)

        link = True

        with bpy.data.libraries.load(filepath, link=link) as (data_from, data_to):
            data_to.objects = data_from.objects

        for obj in data_to.objects:
            if obj is not None:
                scene.objects.link(obj)

        for obj in objects:
            if obj.type == 'CAMERA':
                obj.select = 1
                scene.camera = obj

        bpy.ops.file.make_paths_relative()

        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        self.blendpath = bpy.path.abspath(context.blend_data.filepath)
        bpy.ops.wm.open_mainfile(filepath=self.blendpath)

        return {'FINISHED'}

class PRJDaihatsuRenderPath(bpy.types.Operator):
    'Auto Setup Render Path for Daihatsu Comp File'
    bl_idname='set.daihatsurenderpath'
    bl_label='SetDaihatsuRenderPath'

    def execute(self, context):
        scene = bpy.context.scene
        render = scene.render
        parentdir = bpy.path.abspath(bpy.context.blend_data.filepath)
        parentdir = os.path.abspath(os.path.join(os.path.dirname(parentdir)))
        parentdir = os.path.basename(parentdir)
        parentdir = os.path.splitext(parentdir)[0]
        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        filename = os.path.splitext(filename)[0]

        for obj in bpy.context.scene.objects:
            if obj.type == 'CAMERA':
                obj.name = "CAM_" + filename

        scene.name = filename + "_scene"

        if filename :
            render.filepath = os.path.join("//../../../render/frames/", parentdir, filename, filename + "_")
        else:
            self.report({'ERROR'}, "File is not saved")

        if parentdir == "work_habit_02":

            render.fps = 25
            render.image_settings.file_format = 'PNG'
            render.image_settings.color_mode = 'RGBA'
            render.image_settings.compression = 70
            render.use_shadows = 0
            render.use_sss = 0
            render.use_envmaps = 0
            render.use_raytrace =  0
            render.alpha_mode = 'TRANSPARENT'
            render.antialiasing_samples = '16'
            render.use_edge_enhance = 1
            render.edge_threshold = 1
            render.use_stamp = 0
            render.use_freestyle = 1
            render.resolution_x = 1920
            render.resolution_y = 1080

            # renderlayer auto stuff
            # first removing lineset
            for r in bpy.context.scene.render.layers:
                for ln in r.freestyle_settings.linesets:
                    ln.linestyle.user_clear()
                    r.freestyle_settings.linesets.remove(ln)

            # automating stuff
            for s in bpy.data.scenes:
                for l in s.render.layers:
                    l.use_pass_normal = 1
                    l.use_pass_vector = 1
                    l.use_freestyle = 1
                    l.use_halo = 0
                    l.use_ztransp = 1
                    l.use_sky = 0
                    l.use_strand = 0
                    l.freestyle_settings.use_smoothness = 1
                    l.freestyle_settings.use_culling = 1
                    l.freestyle_settings.use_view_map_cache = 1
                    l.freestyle_settings.linesets.new('lineset')
                    for lineset in l.freestyle_settings.linesets:
                        lineset.select_border = 0
                        lineset.linestyle.name = 'LineStyle'
                        lineset.linestyle.use_fake_user = 1
        else:
            render.fps = 25
            render.image_settings.file_format = 'PNG'
            render.image_settings.color_mode = 'RGBA'
            render.image_settings.compression = 70
            render.use_shadows = 0
            render.use_sss = 0
            render.use_envmaps = 0
            render.use_raytrace =  0
            render.alpha_mode = 'TRANSPARENT'
            render.antialiasing_samples = '16'

        #smart tile size render -- quite fancy name buahahaha
        render_x = render.resolution_x
        render_y = render.resolution_y
        render_percentage = render.resolution_percentage

        if render.resolution_percentage == render_percentage and render.resolution_percentage != 100:
            render.tile_x = render_percentage * render_x / 100 / 4
            render.tile_y = render_percentage * render_y / 100 / 3
        else:
            render.tile_x = render_percentage * render_x / 100 / 2
            render.tile_y = render_percentage * render_y / 100 / 2

        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

        return {'FINISHED'}

class PSSetRenderPath(bpy.types.Operator):
    'Automatic Define Path for Rendering (for most project)'
    bl_idname='set.renderpath'
    bl_label='SetRenderPath'

    @classmethod
    def poll(cls, context):
        return bpy.data.filepath != ""

    def execute(self, context):
        scene = bpy.context.scene
        render = scene.render
        cycles = scene.cycles
        use_nodes = scene.use_nodes
        tree = scene.node_tree
        nodes = tree.nodes
        links = tree.links
        #TODO :separate between internal render and cycles
        #cycles.film_transparent = 1
        render.fps = 25
        render.use_placeholder = 1
        render.display_mode = 'NONE'
        #render.resolution_y = 720
        #render.resolution_x = 1280
        render.resolution_percentage = 100
        render.pixel_aspect_x = 1
        render.pixel_aspect_y = 1
        render.use_antialiasing = True
        render.use_stamp = False
        render.use_simplify = False
        render.antialiasing_samples = '8'
        render.image_settings.compression = 90
        render.image_settings.file_format = 'PNG'
        render.image_settings.color_mode = 'RGBA'
        render.alpha_mode = 'TRANSPARENT'

        if scene.cgru:
            scene.cgru.adv_options = True
            scene.cgru.relativePaths = True
            scene.cgru.pause = True
            for scn in bpy.data.scenes:
                totalFrame = scn.frame_end - scn.frame_start
                if totalFrame >= 150:
                    scene.cgru.fpertask = 5
                else:
                    scene.cgru.fpertask = 10
            if bpy.path.basename(bpy.data.filepath).endswith("_light.blend"):
                filename = bpy.path.basename(bpy.context.blend_data.filepath)
                filename = os.path.splitext(filename)[0]
                filename = filename.split('_light')
                filename = filename[0]
                filename = filename[2:4]
                priority = 251 - int(filename)
                for scn in bpy.data.scenes:
                    scn.cgru.priority = priority

        #drv_seed = bpy.context.scene.driver_add('cycles.seed')
        #drv_seed.driver.type = 'SCRIPTED'
        #drv_seed.driver.expression = "frame"

        parentdir = bpy.path.abspath(bpy.context.blend_data.filepath)
        parentdir = os.path.abspath(os.path.join(os.path.dirname(parentdir)))
        parentdir = os.path.basename(parentdir)
        parentdir = os.path.splitext(parentdir)[0]
        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        filename = os.path.splitext(filename)[0]
        filename = bpy.path.basename(bpy.context.blend_data.filepath)

        if filename:
            if filename.find('_') != -1:
                filename = filename.split('_')
                filename = filename[0]
                bpy.context.scene.render.filepath = os.path.join("//../../render/frames", filename, filename + "_")
            else:
                bpy.context.scene.render.filepath = os.path.join("//../../render/frames", filename, filename + "_")

        if bpy.path.basename(bpy.data.filepath).endswith("_light.blend"):
            filename = bpy.path.basename(bpy.context.blend_data.filepath)
            filename = os.path.splitext(filename)[0]
            filename = filename.split('_light')
            filename = bpy.path.ensure_ext(filename[0], ext = '.blend')
            blendpath = bpy.path.abspath (bpy.context.blend_data.filepath)
            blenddir, blendfile= os.path.split(blendpath)
            filepath = os.path.join(blenddir + '/' + filename)

            orig_frameStart, orig_frameEnd, origScene = blend_render_info.read_blend_rend_chunk(filepath)[0]
            scene.frame_start = orig_frameStart
            scene.frame_end = orig_frameEnd
            scene.name = origScene

        if filename.find('_') != -1:
            filename = filename.split('_')
            filename = filename[0]

        path = render.filepath
        path = path.split('_')
        path = path[0]
        path = path.split(filename)
        path = path[0]

        if use_nodes:
            nodeOutput = nodes.get('fg', None)
            if nodeOutput is None:
                for node in nodes:
                    if node.type == 'R_LAYERS':
                        output_file = nodes.new('CompositorNodeOutputFile')
                        output_file.label = node.layer
                        output_file.name = node.layer
                        output_file.location = 500,200
                        outputIndex = nodes.new('CompositorNodeOutputFile')
                        outputIndex.label = 'mask'
                        outputIndex.name = 'fgIndex'
                        outputIndex.location = 700,300

                        links.new(
                            node.outputs['Image'],
                            output_file.inputs['Image']
                            )
                        links.new(
                            node.outputs['IndexMA'],
                            outputIndex.inputs['Image']
                            )
                    elif node.type == 'OUTPUT_FILE':
                        node.base_path = path + filename + '/' + node.label + '/'
                        fileSlot = node.file_slots.get('Image', None)
                        if fileSlot is not None:
                            fileSlot.path = node.label + '_' + filename + '_'

            unusedNode = nodes.get('fgIndex.001', None)
            if unusedNode is not None:
                nodes.remove(unusedNode)
            #bpy.context.scene.render.filepath = os.path.join("//../../render/", parentdir, filename, filename + "_")
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

        return {'FINISHED'}

class PSOpenglTools(bpy.types.Operator):
    'Automatic OpenGL Render for most projects'
    bl_idname='opengl.toggle'
    bl_label='OpenglToggle'

    def execute(self,context):
        scene = bpy.context.scene
        render = scene.render
        space = bpy.context.space_data

        setcamera(context)
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        space.show_only_render = 1
        scene.frame_step = 1
        #scene.game_settings.material_mode = 'GLSL'
        #bpy.context.space_data.viewport_shade = 'MATERIAL'
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
        render.stamp_background = (0,0,0,0.25)
        render.stamp_foreground = (1,1,1,1)
        #render.antialiasing_samples = '16'
        render.alpha_mode = 'SKY'
        render.use_raytrace = 0
        render.use_envmaps = 0
        render.use_sss = 0
        render.tile_x = 256
        render.tile_y = 256
        render.use_overwrite = 1
        render.use_file_extension = 1
        render.use_placeholder = 1
        render.fps = 25
        render.resolution_percentage = 50
        #render.resolution_x = 1920
        #render.resolution_y = 1080
        render.use_simplify = 1
        render.simplify_subdivision = 0
        render.image_settings.file_format = 'FFMPEG'
        render.ffmpeg.format = 'MPEG4'
        render.ffmpeg.codec = 'H264'
        render.ffmpeg.audio_codec = 'AAC'
        #render.image_settings.compression = 100
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

        if filename:
            if filename.find('_') != -1:
                filename = filename.split('_')
                filename = filename[0]
                bpy.context.scene.render.filepath = os.path.join("//../../render/playblast/", filename + ".mp4")
            else:
                bpy.context.scene.render.filepath = os.path.join("//../../render/playblast/", filename + ".mp4")

        bpy.ops.render.opengl(animation = 1)
        bpy.ops.render.play_rendered_anim()

        self.blendpath = bpy.path.abspath(context.blend_data.filepath)
        bpy.ops.wm.open_mainfile(filepath=self.blendpath)

        return {'FINISHED'}

class PSShadelessToggle(bpy.types.Operator):
    'Toggle Shadeless'
    bl_idname='shadeless.toggle'
    bl_label='Shadeless Toggle'

    ##TODO : need to define poll for internal render only

    def execute(self, context):
        for m in context.active_object.material_slots:
            for e in context.selected_objects:
                for o in e.material_slots:
                    if m.material.use_shadeless == 0:
                        o.material.use_shadeless = 1
                        context.scene.game_settings.material_mode = 'GLSL'
        return {'FINISHED'}

class PSGridToggle(bpy.types.Operator):
    'Toggle Grid'
    bl_idname = 'grid.toggle'
    bl_label = 'Toggle Grid'

    def execute(self, context):
        space = bpy.context.space_data

        if space.show_floor == 1:
            space.show_floor = 0
            space.show_axis_x = 0
            space.show_axis_y = 0
            space.show_axis_z = 0
        else:
            space.show_floor = 1
            space.show_axis_x = 1
            space.show_axis_y = 1
            space.show_axis_z = 0
        return {'FINISHED'}

class PSSetFrames(bpy.types.Operator):
    'Use current scenes frame start and end for all scenes available'
    bl_idname='setframes.toggle'
    bl_label='Set Frames'

    def execute(self, context):
        sf = bpy.context.scene.frame_start
        ef = bpy.context.scene.frame_end

        for n in bpy.data.scenes:
            n.frame_start = sf
            n.frame_end = ef

        return {'FINISHED'}

class PSBoundstoTextured(bpy.types.Operator):
    'Quick switching selected objects draw type from bounds to textured or vice versa'
    bl_idname='boundstextured.toggle'
    bl_label='Bounds to Textured Toggle'

    def execute(self, context):
        s = bpy.context.active_object.draw_type
        for o in bpy.context.selected_objects:
            if s == 'BOUNDS':
                o.draw_type = 'TEXTURED'
            else:
                o.draw_type = 'BOUNDS'
        return {'FINISHED'}

class PSSwitchRenderResolution(bpy.types.Operator):
    'Quick Switching Render Resolution'
    bl_idname='renderres.toggle'
    bl_label='Render Resolution Switching Toggle'

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

class PSSimplifyMenu(bpy.types.Operator):
    bl_idname = "scene.simplify"
    bl_label = "Simplify!"

    def execute(self, context):
        render = bpy.context.scene.render
        render.simplify_subdivision = 0

        if render.use_simplify:
            render.use_simplify = 0
        else:
            render.use_simplify = 1
        return {'FINISHED'}

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

#--copied from useless-tools
class PSRecalcNormalsObjects(bpy.types.Operator):

    'Recalculate normals of all selected objects'
    bl_idname = 'ps.recalculate_normals'
    bl_label = 'Recalculate Normals'

    @classmethod
    def poll(cls, context):
        return bpy.context.mode == 'OBJECT' and bpy.context.selected_objects

    def execute(self, context,):
        objs = context.selected_objects
        oldactive = context.active_object

        for obj in objs:
            context.scene.objects.active = obj
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=0)
            bpy.ops.object.editmode_toggle()
            self.report({'INFO'}, "Recalculated normals of " + obj.name)
        return {'FINISHED'}

class PSSaveFile(bpy.types.Operator):

    'Saves the File, or Save As if not saved already'
    bl_idname = 'ps.save_file'
    bl_label = 'Save File'

    @classmethod
    def poll(cls, context):
        return bpy.data.filepath != "" and not bpy.data.filepath.endswith("untitled.blend")

    def execute(self, context,):
        if bpy.data.filepath != "":
            bpy.ops.wm.save_mainfile(filepath=bpy.data.filepath)
        else:
            bpy.ops.wm.save_as_mainfile()
        return {'FINISHED'}

class KMSSaveProgress(bpy.types.Operator):
    'Saves the copy inside progress directory and open it'
    bl_idname = 'ps.save_progress'
    bl_label = 'Save Copy in Progress'

    @classmethod
    def poll (self, context):
        return context.blend_data.is_saved\
            and not bpy.data.filepath[-7:-6].isnumeric()

    def execute(self, context):
        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        filename = os.path.splitext(filename)[0]

        blendpath = bpy.path.abspath (bpy.context.blend_data.filepath)
        blenddir, blendfile = os.path.split(blendpath)
        progressdir = os.path.join(blenddir, 'progress_' + filename)

        if not os.path.exists(progressdir):
            os.makedirs(progressdir)

        if os.path.exists(progressdir) and not os.listdir(progressdir) == []:
            self.report({'INFO'}, "Progress Folder Available, Please Open File ")

        else:
            progresspath = bpy.path.ensure_ext(
                filepath = os.path.join(progressdir, filename + '_01'), ext = ".blend")

            bpy.data.use_autopack = 0
            bpy.ops.wm.save_as_mainfile(filepath=progresspath, copy = 1, relative_remap = 1, compress= 1)
            bpy.ops.wm.open_mainfile(filepath=progresspath)

        return {'FINISHED'}

class KMSSaveFileIncrement(bpy.types.Operator):

    'Increments the file name and then saves it'
    bl_idname = 'ps.save_file_increment'
    bl_label = 'Save File Increment'

    @classmethod
    def poll(cls, context):
        return bpy.data.filepath[-7:-6].isnumeric()

    def execute(self, context,):
        if bpy.data.filepath != "":
            fp = bpy.data.filepath
            enddigit = fp[-7:-6]
            end2digit = fp[-8:-7]
            end3digit = fp[-9:-8]

            if enddigit.isnumeric():
                if int(enddigit) == 9 and not end2digit.isnumeric():
                    endint = int(enddigit) + 1
                    fp = fp[:-7] + str(endint) + fp[-6:]
                if int(enddigit) != 9:
                    endint = int(enddigit) + 1
                    fp = fp[:-7] + str(endint) + fp[-6:]
                if end2digit.isnumeric() and int(enddigit) == 9:
                    endint = 0
                    end2int = int(end2digit) + 1
                    fp = fp[:-8] + str(end2int) + str(endint) + fp[-6:]
                if end3digit.isnumeric() and int(end2digit) == 9 and int(enddigit) == 9:
                    endint = 0
                    end2int = 0
                    end3int = int(end3digit) + 1
                    fp = fp[:-10] + str(end3int) + str(end2int) + str(endint) + fp[-6:]
            splitsep = fp.split(os.sep)
            self.report({'INFO'}, "Saved as " + splitsep[len(splitsep) - 1])
            bpy.ops.wm.save_as_mainfile(filepath=fp)
            # To Do : also copy it to original file, if there available
            filename = bpy.path.basename(bpy.context.blend_data.filepath)
            filename = os.path.splitext(filename)[0]
            #remove any numbering
            base_dot = filename[::-1].split('.', maxsplit=1)[-1][::-1]
            base_under = filename[::-1].split('_', maxsplit=1)[-1][::-1]
            base_dash = filename[::-1].split('-', maxsplit=1)[-1][::-1]
            base_sep = filename[::-1].split((context.scene.RNSeparator[::-1]), maxsplit=1)[-1][::-1]
            strings=[base_dot, base_under, base_dash, base_sep]
            shortest_base=min(strings, key=len)
            blendpath = bpy.path.abspath (bpy.context.blend_data.filepath)
            blenddir, blendfile = os.path.split(blendpath)
            oripath = os.path.join(blenddir, '..')
            copypath = bpy.path.ensure_ext(
                filepath = os.path.join(oripath, shortest_base), ext = ".blend")
            bpy.ops.wm.save_as_mainfile(filepath=copypath, copy = 1, relative_remap = 1)

        else:
            print("saving as...")
            bpy.ops.wm.save_as_mainfile()
        return {'FINISHED'}

class KMSPositionedSuzanne(bpy.types.Operator):
    'Adjust monkey to sit on the ground'
    bl_idname = 'ps.position_suz'
    bl_label = 'Suzanne Sit'

    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT')

    def execute(self, context):
        cloc = bpy.context.scene.cursor_location
        objs = bpy.context.selected_objects

        for o in objs:
            if o.name == "Suzanne":
                o.location.x = cloc.x
                o.location.y = cloc.y
                o.location.z = cloc.z+0.4955
                bpy.ops.object.shade_smooth()
                bpy.ops.object.subdivision_set(level=3)
                bpy.context.object.modifiers["Subsurf"].render_levels = 3
                bpy.context.object.rotation_euler.x = -0.6254132986068726
        return {'FINISHED'}

def info_scene(self, context):
    filename = bpy.path.basename(bpy.context.blend_data.filepath)
    filename = os.path.splitext(filename)[0]
    layout = self.layout

    col=layout.column()
    if not context.blend_data.is_saved:
        col.label(text="File is not saved", icon='SCENE_DATA')
    elif context.blend_data.is_dirty == 1:
        col.label(text=" %s*" % (filename), icon='SCENE_DATA')
    else :
        col.label(text=" %s" % (filename), icon='SCENE_DATA')

def register():
    bpy.types.Scene.RNSeparator = bpy.props.StringProperty(
        name="Separator",
        default="_",
        description="The bit between the base name and incremented number")

    bpy.utils.register_module(__name__)
    bpy.types.INFO_HT_header.prepend(info_scene)


def unregister():
    del bpy.types.Scene.RNSeparator

    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_HT_header.remove(info_scene)

if __name__ == "__main__":
    register()
