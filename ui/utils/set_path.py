import bpy

def setpath(self, context):
    layout = self.layout

    col = layout.column()
    row = col.row(align=True)

    row.operator(
        "set.renderpath",
        text="Set Path",
        icon="FILE_FOLDER")
