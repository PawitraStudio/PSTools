import bpy

class PSBoundstoTextured(bpy.types.Operator):
    'Quick switching selected objects draw type\
    from bounds to textured or vice versa'
    bl_idname = 'boundstextured.toggle'
    bl_label = 'Bounds to Textured Toggle'

    def execute(self, context):
        s = bpy.context.active_object.draw_type
        for o in bpy.context.selected_objects:
            if s == 'BOUNDS':
                o.draw_type = 'TEXTURED'
            else:
                o.draw_type = 'BOUNDS'
        return {'FINISHED'}