import bpy

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