import bpy

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