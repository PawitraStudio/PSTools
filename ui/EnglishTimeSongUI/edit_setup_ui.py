import bpy

def KSEditSetup(self, context):
    layout = self.layout
    # col = layout.column()
    # row = col.row(align=True)
    split = layout.split(percentage=0.66)
    split.label(text="Only for Kidsong Edit:")

    row = split.row(align=True)
    row.operator(
        "set.ksedit",
        text="RENDER!!!",
        icon="PLAY"
    )