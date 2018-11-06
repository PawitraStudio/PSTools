import bpy
import os

class PSSetRenderPath(bpy.types.Operator):
    'Automatic Define Path for Rendering (for most project)'
    bl_idname = 'set.renderpath'
    bl_label = 'SetRenderPath'

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
        # TODO :separate between internal render and cycles
        # cycles.film_transparent = 1
        # render.fps = 25
        # render.use_placeholder = 1
        # render.display_mode = 'NONE'
        # # render.resolution_y = 720
        # # render.resolution_x = 1280
        # render.resolution_percentage = 100
        # render.pixel_aspect_x = 1
        # render.pixel_aspect_y = 1
        # render.use_antialiasing = True
        # render.use_stamp = False
        # render.use_simplify = False
        # render.antialiasing_samples = '8'
        # render.image_settings.compression = 90
        # render.image_settings.file_format = 'PNG'
        # render.image_settings.color_mode = 'RGBA'
        # render.alpha_mode = 'TRANSPARENT'

        # if scene.cgru:
        #     scene.cgru.adv_options = True
        #     scene.cgru.relativePaths = True
        #     scene.cgru.pause = True
        #     for scn in bpy.data.scenes:
        #         totalFrame = scn.frame_end - scn.frame_start
        #         if totalFrame >= 150:
        #             scene.cgru.fpertask = 5
        #         else:
        #             scene.cgru.fpertask = 10
        #     if bpy.path.basename(bpy.data.filepath).endswith("_light.blend"):
        #         filename = bpy.path.basename(bpy.context.blend_data.filepath)
        #         filename = os.path.splitext(filename)[0]
        #         filename = filename.split('_light')
        #         filename = filename[0]
        #         filename = filename[2:4]
        #         priority = 251 - int(filename)
        #         for scn in bpy.data.scenes:
        #             scn.cgru.priority = priority

        # drv_seed = bpy.context.scene.driver_add('cycles.seed')
        # drv_seed.driver.type = 'SCRIPTED'
        # drv_seed.driver.expression = "frame"

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
                bpy.context.scene.render.filepath = os.path.join(
                    "//../../render/frames",
                    filename,
                    filename + "_")
            else:
                bpy.context.scene.render.filepath = os.path.join(
                    "//../../render/frames",
                    filename,
                    filename + "_")

        # if bpy.path.basename(bpy.data.filepath).endswith("_light.blend"):
        #     filename = bpy.path.basename(bpy.context.blend_data.filepath)
        #     filename = os.path.splitext(filename)[0]
        #     filename = filename.split('_light')
        #     filename = bpy.path.ensure_ext(filename[0], ext='.blend')
        #     blendpath = bpy.path.abspath(bpy.context.blend_data.filepath)
        #     blenddir, blendfile = os.path.split(blendpath)
        #     filepath = os.path.join(blenddir + '/' + filename)

        #     orig_frameStart,
        #     orig_frameEnd,
        #     origScene = blend_render_info.read_blend_rend_chunk(filepath)[0]
        #     scene.frame_start = orig_frameStart
        #     scene.frame_end = orig_frameEnd
        #     scene.name = origScene

        # if filename.find('_') != -1:
        #     filename = filename.split('_')
        #     filename = filename[0]

        # path = render.filepath
        # path = path.split('_')
        # path = path[0]
        # path = path.split(filename)
        # path = path[0]

        # if use_nodes:
        #     nodeOutput = nodes.get('fg', None)
        #     if nodeOutput is None:
        #         for node in nodes:
        #             if node.type == 'R_LAYERS':
        #                 output_file = nodes.new('CompositorNodeOutputFile')
        #                 output_file.label = node.layer
        #                 output_file.name = node.layer
        #                 output_file.location = 500, 200
        #                 outputIndex = nodes.new('CompositorNodeOutputFile')
        #                 outputIndex.label = 'mask'
        #                 outputIndex.name = 'fgIndex'
        #                 outputIndex.location = 700, 300

        #                 links.new(
        #                     node.outputs['Image'],
        #                     output_file.inputs['Image']
        #                     )
        #                 links.new(
        #                     node.outputs['IndexMA'],
        #                     outputIndex.inputs['Image']
        #                     )
        #             elif node.type == 'OUTPUT_FILE':
        #                 node.base_path = path + filename\
        #                     + '/' + node.label + '/'
        #                 fileSlot = node.file_slots.get('Image', None)
        #                 if fileSlot is not None:
        #                     fileSlot.path = node.label + '_' + filename + '_'

        #     unusedNode = nodes.get('fgIndex.001', None)
        #     if unusedNode is not None:
        #         nodes.remove(unusedNode)
            # bpy.context.scene.render.filepath = os.path.join(
            #   "//../../render/", parentdir, filename, filename + "_")
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

        return {'FINISHED'}