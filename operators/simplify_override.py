import bpy

class PSSimplifyMenu(bpy.types.Operator):
    bl_idname = "scene.simplify"
    bl_label = "Simplify!"

    def execute(self, context):
        render = bpy.context.scene.render
        render.simplify_subdivision = 0

        if render.use_simplify:
            render.use_simplify = 0
        else:
            render.use_simplify = 1
        return {'FINISHED'}