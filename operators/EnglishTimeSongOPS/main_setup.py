import bpy
import os

class KSAutoSetup(bpy.types.Operator):
    'Automatic Setup Operators for Kidsong Project'
    bl_idname = 'set.ksrender'
    bl_label = 'SetKSRender'

    # kode ini utk memastikan filenya ada dan telah disimpan
    @classmethod
    def poll(cls, context):
        return bpy.data.filepath != ""\
            and bpy.context.scene.render.engine == 'CYCLES'

    def execute(self, context):
        scene = bpy.context.scene
        render = scene.render
        cycles = scene.cycles
        actions = bpy.data.actions

        for action in actions:
            action.use_fake_user = 1
        # use_nodes = scene.use_nodes
        # tree = scene.node_tree
        # nodes = tree.nodes
        # links = tree.links

        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        filename = filename.split('.')
        namafile = filename[0]
        episode = (namafile[3]+namafile[4])

        # semua setting scene
        # scene.view_settings.exposure = 1.2
        # scene.view_settings.gamma = 0.8
        # scene.world.light_settings.ao_factor = 0.1
        # scene.world.light_settings.distance = 10
        # scene.world.light_settings.use_ambient_occlusion = 1

        # semua setting render
        render.engine = 'CYCLES'
        render.resolution_x = 1920
        render.resolution_y = 1080
        render.resolution_percentage = 100
        render.tile_x = 240
        render.tile_y = 216
        # render.use_compositing =  1
        render.use_sequencer = 0
        render.use_simplify = 1
        render.simplify_subdivision_render = 6

        # semua setting cycles
        cycles.device = 'GPU'
        cycles.progressive = 'BRANCHED_PATH'
        cycles.aa_samples = 32
        cycles.sample_clamp_indirect = 1
        cycles.film_transparent = True
        cycles.sample_clamp_indirect = 1
        cycles.ao_bounces = 3
        cycles.ao_bounces_render = 3

        # enable the layer
        for scn in bpy.data.scenes:
            scn.layers[0] = 1
            scn.layers[1] = 0
            scn.layers[2] = 0
            scn.layers[3] = 0
            scn.layers[4] = 0
            scn.layers[5] = 1
            scn.layers[6] = 0
            scn.layers[7] = 0
            scn.layers[8] = 0
            scn.layers[9] = 0
            scn.layers[10] = 1
            scn.layers[11] = 0
            scn.layers[12] = 0
            scn.layers[13] = 0
            scn.layers[14] = 0
            scn.layers[15] = 1
            scn.layers[16] = 0
            scn.layers[17] = 0
            scn.layers[18] = 0
            scn.layers[19] = 0

        # aktivasi denoising
        for layer in render.layers:
            layer.cycles.use_denoising = 1

		#file save
        bpy.context.scene.render.filepath = "x:\\PROJECTS\\20170910_english_time_song\\03_post\\render\\"+episode+"\\"+namafile+"\\"+namafile+"_"""

        return {'FINISHED'}