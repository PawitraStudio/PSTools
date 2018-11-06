import bpy
import os

class KMSSaveProgress(bpy.types.Operator):
    'Saves the copy inside progress directory and open it'
    bl_idname = 'ps.save_progress'
    bl_label = 'Save Copy in Progress'

    @classmethod
    def poll(self, context):
        return context.blend_data.is_saved\
            and not bpy.path.display_name_from_filepath(
                                os.path.normpath(
                                    os.path.join(
                                        bpy.data.filepath, os.pardir
                                        ))).startswith("WIP_")
            #and not bpy.data.filepath[-7:-6].isnumeric()

    def execute(self, context):
        filename = bpy.path.basename(bpy.context.blend_data.filepath)
        filename = os.path.splitext(filename)[0]

        blendpath = bpy.path.abspath(bpy.context.blend_data.filepath)
        blenddir, blendfile = os.path.split(blendpath)
        progressdir = os.path.join(blenddir, 'WIP_' + filename)

        if not os.path.exists(progressdir):
            os.makedirs(progressdir)

        if os.path.exists(progressdir) and not os.listdir(progressdir) == []:
            self.report(
                {'INFO'},
                "WIP Folder Available, Please Open File ")

        else:
            progresspath = bpy.path.ensure_ext(
                filepath=os.path.join(
                    progressdir,
                    filename + '_v01'),
                ext=".blend")

            bpy.data.use_autopack = 0
            bpy.ops.wm.save_as_mainfile(
                filepath=progresspath,
                copy=1,
                relative_remap=1,
                compress=1)
            bpy.ops.wm.open_mainfile(filepath=progresspath)

        return {'FINISHED'}