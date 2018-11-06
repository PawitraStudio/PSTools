import bpy

class PSShadelessToggle(bpy.types.Operator):
    'Toggle Shadeless'
    bl_idname = 'shadeless.toggle'
    bl_label = 'Shadeless Toggle'

    # TODO : need to define poll for internal render only

    def execute(self, context):
        for m in context.active_object.material_slots:
            for e in context.selected_objects:
                for o in e.material_slots:
                    if m.material.use_shadeless == 0:
                        o.material.use_shadeless = 1
                        context.scene.game_settings.material_mode = 'GLSL'
        return {'FINISHED'}