import bpy

def get_panels(self, context):  # pylint: disable=unused-argument
    return [
            ("MAIN", "Main", "Main", "EXPORT", 0),
            ("RUV_SETTINGS", "RUV Settings", "RUV Settings", "MEMORY", 1),
            ("SETTINGS", "Addon Settings", "Addon Settings", "PREFERENCES", 3),
        ]

def get_maps(self, context):
    act_obj = bpy.context.active_object
    items = []

    if act_obj and act_obj.type == "MESH":
        pass

    else:
        return [("NO_OBJ", "INFO: No Active Object", "",'ERROR',0)]

    if act_obj.data.uv_layers:
        for uvmap in act_obj.data.uv_layers:
            items.append((uvmap.name, uvmap.name, "",'UV',0))

    else:
        return [("NO_MAP", "INFO: No UV Maps", "")]

    global RUV_ITEMS
    RUV_ITEMS = items

    return items

def uv_map_update(self, context):  # pylint: disable=unused-argument
    maps = context.window_manager.RUV_Context
    act_obj = bpy.context.active_object

    if act_obj and act_obj.type == "MESH":
        act_obj.data.uv_layers.active = act_obj.data.uv_layers[maps.uv_maps]

    else:
        pass

def get_scripts(self, context):

    props = bpy.context.preferences.addons["RUV"].preferences

    if props.settings:
        items = [
            ("NO_SCRIPT", "No Script", "Exports current UV layout in its present condition","OUTLINER_DATA_LIGHTPROBE",0),
            ("FLATTEN", "Reset UVs", "Reset all UV maps in Rizom, all seams will be welded.","RECOVER_LAST",1),
            (
                "SHARP_EDGES",
                "Sharp Edges",
                "Performs a quick auto unwrap using the sharp edges algorithm",
                "SCULPTMODE_HLT",
                2,
            ),
            (
                "PELT",
                "Pelt",
                "Performs a quick auto unwrap using the pelt algorithm",
                "OUTLINER_OB_ARMATURE",
                3,
            ),
            (
                "MOSAIC",
                "Mosaic",
                "Performs a quick auto unwrap using the mosaic algorithm",
                "MESH_CYLINDER",
                4,
            ),
            (
                "BOX",
                "Box",
                "Performs a quick auto unwrap using the box algorithm",
                "MOD_EXPLODE",
                5,
            ),
        ]

    elif not props.settings:
        items = [
            ("NO_SCRIPT", "No Script", "Exports current UV layout in its present condition","OUTLINER_DATA_LIGHTPROBE",0),
            ("FLATTEN", "Reset UVs", "Reset all UV maps in Rizom, all seams will be welded.","RECOVER_LAST",1),
        ]

    return items

def script_check(self, context):  # pylint:
    props = bpy.context.preferences.addons["RUV"].preferences
    if not props.settings:
        if props.script not in ("NO_SCRIPT", "FLATTEN"):
            props.script = "NO_SCRIPT"

def opt_AutoIMP(self,context):
    return [
        ('N_AutoIMP','Manual','Manually imported UVs','MODIFIER',0),
        ('Y_AutoIMP','Auto','Automatically imported after closing RizomUV','CONSTRAINT',1),
    ]

def preference_save(self, context):  # pylint: disable=unused-argument
    bpy.ops.wm.save_userpref()

def shortcut(self, context):
    return [
        ("11",'Blender mix 3DsMax',""),
        ("0",'Rizom',""),
        ("1",'Rizom Legacy',""),
        ("2",'Maya',""),
        ("3",'3DsMax',""),
        ("4",'Softimage',""),
        ("5",'Rhino',""),
        ("6",'Cinemar4D',""),
        ("7",'Blender',""),
        ("8",'ZBrush',""),
        ("9",'Modo',""),
        ("10",'RMB Orbit',""),
    ]

def panel_width_update(self, context):
    bpy.context.area.tag_redraw()