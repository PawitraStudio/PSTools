import bpy

def PSFileFunction(self, context):
    layout = self.layout

    col = layout.column()
    row = col.row(align=True)

    row.alignment = 'CENTER'
    row.operator(
        "wm.window_fullscreen_toggle",
        icon="FULLSCREEN_ENTER",
        text="")
    # row.operator(
    #     "wm.quit_blender",
    #     icon="QUIT",
    #     text="")
    row.operator(
        "ps.save_file",
        icon="FILE_TICK",
        text="")
    row.operator(
        "ps.save_progress",
        icon="OPEN_RECENT",
        text="")
    row.operator(
        "ps.save_file_increment",
        icon="ZOOMIN",
        text="")
    row.operator(
        "wm.save_as_mainfile",
        icon="SAVE_AS",
        text="")
    row.operator(
        "wm.open_mainfile",
        icon="FILE_FOLDER",
        text="")
    row.operator(
        "wm.link",
        icon="LINK_BLEND",
        text="")
    row.operator(
        "wm.append",
        icon="APPEND_BLEND",
        text="")
    row.operator(
        "shots.relink",
        icon="LIBRARY_DATA_DIRECT",
        text="")