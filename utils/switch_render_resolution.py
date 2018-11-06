import bpy

def PSSwitchRenderResolution(self, context):
    layout = self.layout
    col = layout.column(align=True)
    col.operator(
        "renderres.toggle",
        text='Switch Resolution',
        icon='FILE_REFRESH')