import bpy
import os

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
                if end3digit.isnumeric() and\
                        int(end2digit) == 9 and\
                        int(enddigit) == 9:
                    endint = 0
                    end2int = 0
                    end3int = int(end3digit) + 1
                    fp = fp[:-10]
                    + str(end3int)
                    + str(end2int)
                    + str(endint)
                    + fp[-6:]
            splitsep = fp.split(os.sep)
            self.report({'INFO'}, "Saved as " + splitsep[len(splitsep) - 1])
            bpy.ops.wm.save_as_mainfile(filepath=fp)
            # To Do : also copy it to original file, if there available
            filename = bpy.path.basename(bpy.context.blend_data.filepath)
            filename = os.path.splitext(filename)[0]
            # remove any numbering
            base_dot = filename[::-1].split('.', maxsplit=1)[-1][::-1]
            base_under = filename[::-1].split('_', maxsplit=1)[-1][::-1]
            base_dash = filename[::-1].split('-', maxsplit=1)[-1][::-1]
            base_sep = filename[::-1].split(
                (context.scene.RNSeparator[::-1]), maxsplit=1)[-1][::-1]
            strings = [base_dot, base_under, base_dash, base_sep]
            shortest_base = min(strings, key=len)
            blendpath = bpy.path.abspath(bpy.context.blend_data.filepath)
            blenddir, blendfile = os.path.split(blendpath)
            oripath = os.path.join(blenddir, '..')
            copypath = bpy.path.ensure_ext(
                filepath=os.path.join(oripath, shortest_base),
                ext=".blend")
            bpy.ops.wm.save_as_mainfile(
                filepath=copypath,
                copy=1,
                relative_remap=1)
        else:
            print("saving as...")
            bpy.ops.wm.save_as_mainfile()
        return {'FINISHED'}