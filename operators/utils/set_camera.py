import bpy

def setcamera(context):
    view3d = bpy.context.space_data.region_3d

    for ob in bpy.context.scene.objects:
        if view3d.view_perspective != 'CAMERA':
            bpy.ops.view3d.viewnumpad(type='CAMERA')
    return setcamera