import bpy

def set_keymap_property(properties, property_name, value):
    try:
        setattr(properties, property_name, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (property_name, properties.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)

def register_shortcuts():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(
                name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(
                'wm.call_menu_pie',
                'E',
                'PRESS', shift=True)
        kmi.properties.name = 'VIEW3D_PIE_pstools'
