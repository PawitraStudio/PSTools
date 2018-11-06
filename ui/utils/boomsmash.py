import bpy

def PSOpenglrender(self, context):
    layout = self.layout

    col = layout.column()
    row = col.row(align=True)

    row.operator(
        "opengl.toggle",
        text='Boomsmash',
        icon="CLIP")