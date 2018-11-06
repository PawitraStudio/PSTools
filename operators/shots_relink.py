import bpy
import os

class PSRelinkShots(bpy.types.Operator):
    'Auto Relink Shots File'
    bl_idname = 'shots.relink'
    bl_label = 'ShotsRelink'

    @classmethod
    def poll(cls, context):
        return bpy.data.filepath != "" and bpy.path.display_name_from_filepath(
                                        bpy.data.filepath).startswith("lg_")

    def execute(self, context):
        objects = bpy.data.objects
        scene = bpy.context.scene

        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        filename = os.path.splitext(filename)[0]
        filename = filename.split('lg_')
        filename = bpy.path.ensure_ext('an_' + filename[1], ext='.blend')

        blendpath = bpy.path.abspath(bpy.context.blend_data.filepath)
        blenddir, blendfile = os.path.split(blendpath)
        filepath = os.path.join(blenddir + '/' + filename)

        for obj in objects:
            if obj.get is not None and obj.type != 'LAMP':
                # obj.select = True
                # else :
                # obj.select = False
                # bpy.ops.object.delete()
                bpy.data.objects.remove(obj, do_unlink=True)

        link = True

        with bpy.data.libraries.load(
            filepath,
            link=link) as (
                data_from,
                data_to):
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