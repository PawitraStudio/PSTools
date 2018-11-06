import bpy

class PSSaveFile(bpy.types.Operator):
    'Saves the File, or Save As if not saved already'
    bl_idname = 'ps.save_file'
    bl_label = 'Save File'

    @classmethod
    def poll(cls, context):
        return bpy.data.filepath != "" and\
         not bpy.data.filepath.endswith("untitled.blend")

    def execute(self, context,):
        if bpy.data.filepath != "":
            bpy.ops.wm.save_mainfile(filepath=bpy.data.filepath)
        else:
            bpy.ops.wm.save_as_mainfile()
        return {'FINISHED'}