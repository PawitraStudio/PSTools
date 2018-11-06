import bpy

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