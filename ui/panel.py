import bpy

class PSTools(bpy.types.Panel):
    bl_label = "PSTools"
    bl_category = "PSTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Setup Tools ")

        col.operator(
            "boundstextured.toggle",
            text="Quick Switch",
            icon="MATERIAL_DATA")
        col.operator(
            "setframes.toggle",
            text="Set Frames",
            icon="TIME")
        col.operator(
            "file.make_paths_relative",
            text="Make Relative",
            icon="LINK_AREA")
        col.operator(
            "file.find_missing_files",
            text="Find Missing",
            icon="ZOOM_ALL")
        col.operator(
            "render.render",
            text="Render",
            icon="RENDER_STILL")
        # col.operator(
        #     "set.renderpath",
        #     text="Set Path",
        #     icon="FILE_FOLDER")
        col.operator(
            "set.ksrender",
            text="Kidsong Setup",
            icon="SCRIPTWIN")

        box = layout.box()
        col = box.column(align=True)
        col.label(text="Boomsmash !")
        row = col.row(align=True)
        row.operator(
            "opengl.toggle",
            text="Fast",
            icon="NEXT_KEYFRAME")
        row.operator(
            "openglhires.toggle",
            text="Smooth",
            icon="MESH_MONKEY")
        row.operator(
            "boomsmash.compare",
            text="Compare",
            icon="CAMERA_STEREO")
        col.operator(
            "scene.simplify",
            text="Simplify",
            icon="META_CUBE")

        row.separator

        view = context.scene.render
        scene = context.scene
        space = context.space_data

        row = layout.row()
        row.prop(view, "use_simplify", text="Simplify")
        sub = row.column()
        sub.active = view.use_simplify
        sub.prop(view, "simplify_subdivision", text="Level")
        row.separator()

        col = layout.column()
        col.prop(space, "show_only_render")
        col.prop(space, "lock_camera")
        col.label(text="Adjust Frame")
        row = layout.row()
        row.prop(context.scene, "frame_start", text="in")
        row.prop(context.scene, "frame_end", text="out")
        row.separator()

        box = layout.box()
        col = box.column(align=True)
        col.label(text="Show")
        row = col.row(align=True)
        row.operator(
            "popup.grapheditor",
             text="Graph Editor",
              icon="IPO"
        )
        row.operator(
            "popup.dopesheet",
             text="DopeSheet",
              icon="ACTION"
        )