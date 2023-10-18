import tempfile, os, bpy
from bpy.props import (StringProperty, BoolProperty,EnumProperty)
from bpy.types import AddonPreferences

from ..operators import utility
from ..context import items

class RUV_AddonPreferences(AddonPreferences):
    bl_idname = "RUV"
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = row.column()
        col.label(text="Tab Category:")
        col.prop(self, "panel_category", text="")

    panel_category: StringProperty(
        name="Panel Tab",
        default="RizomUV",
        description="panel_category",
    )

    rizom_path: StringProperty(
        name="Rizom Path",
        subtype="FILE_PATH",
        default=r'/Applications/RizomUV.2022.0.app',
        update=items.preference_save,
    )

    temp_path: StringProperty(
        name= "fbx path export",
        default= tempfile.gettempdir() + os.sep + "export_temp.fbx",
    )

    lua_path: StringProperty(
         name= "lua scripts path",
         default= os.path.dirname(__file__).replace("context", "scripts") + os.sep,
    )

    settings: BoolProperty(
        name="Enable Settings", default=True, update=items.script_check, description="Toggle Rizom scripts and preferences saving on or off, turning it off will cause scenes to load a little quicker in Rizom.\nThis can be helpful for heavy meshes"
    )

    exclude_linked: BoolProperty(
        name="Exclude Linked", default=False, description="If objects with linked mesh data are selected only export a single copy")

    # Import settings
    replace: BoolProperty(name="Replace Meshes", default=False, description="Replace objects instead of transfering UVs to your original objects.\nThis is useful for occasions where something goes wrong with the FBX export and the vertex order is messed up.\n(MODIFIERS WILL BE DESTROYED)")

    reveal: BoolProperty(name="Show Hidden", default=True, description='If any hidden objects are updated during the import process, make them visible in the Blender viewport')

    seams: BoolProperty(name="Mark Seams", default=False, description="Mark the boundaries of each UV island as seams upon import into Blender")

    sharp: BoolProperty(name="Mark Sharp", default=False, description="Mark the boundaries of each UV island as sharp edges upon import into Blender")


    # Autoseams
    script: EnumProperty(
        name="Script",
        items=(items.get_scripts),
        description="The LUA script that will run when your meshes are loaded into RizomUV",
    )

    luascript: StringProperty(
        name="luascript",
        default= """
            ZomLoad({File={Path="filepath", ImportGroups=true, XYZ=false}, NormalizeUVW=true})

            ZomSet({Path="Vars.Viewport.ColorMapIDDisplayMode", Value=1})
            ZomSet({Path="Prefs.UI.Display.Select", Value=false})
            ZomSet({Path="Prefs.UI.Display.MultiUVSet", Value=false})
            ZomSet({Path="Prefs.UI.Display.AlignStraightenFlip", Value=true})
            ZomSet({Path="Prefs.UI.Display.AutoSelect", Value=true})
            ZomSet({Path="Prefs.UI.Display.Help", Value=false})
            ZomSet({Path="Prefs.UI.Display.Seams", Value=false})
            ZomSet({Path="Prefs.Default.Packing.MaxScaling", Value=1e+06})
            ZomSet({Path="Prefs.Default.Packing.MinScaling", Value=0})
            ZomSet({Path="Prefs.MousePresetMode", Value=2})
            ZomSet({Path="Prefs.PackOptions.MixScales", Value=true})
            ZomSet({Path="Prefs.UI.Display.ScriptLog", Value=false})
            ZomSet({Path="Prefs.UI.Display.PackLayout", Value=true})
            ZomSet({Path="Prefs.UI.Display.UnfoldOptimize", Value=true})
            ZomSet({Path="Prefs.UI.Display.Transform", Value=false})
            ZomSet({Path="Prefs.UI.Display.Proportional", Value=false})
            ZomSet({Path="Prefs.UI.Display.Grid", Value=false})
            ZomSet({Path="Prefs.UI.Display.TileSizeOffset", Value=false})
            ZomSet({Path="Prefs.UI.Display.MultiTile", Value=false})


            ZomSet({Path="Prefs.MousePresetMode", Value=11})
            ZomSet({Path="Prefs.CustomMousePreset",
            Value={ORBIT={MB="MMB", MODS="", KEYCODE=0},
            ZOOM={MB="MMB", MODS="Alt-Ctrl", KEYCODE=0},
            PAN={MB="MMB", MODS="Shift", KEYCODE=0},
            DENSITY_PAINT={MB="LMB", MODS="", KEYCODE=0},
            OPTIMIZE_PAINT={MB="LMB", MODS="", KEYCODE=0},
            PIN_PAINT={MB="LMB", MODS="", KEYCODE=0},
            PROTECT_PAINT={MB="LMB", MODS="", KEYCODE=0},
            UNFOLD_PAINT={MB="LMB", MODS="", KEYCODE=0},
            SPREAD={MB="LMB", MODS="", KEYCODE=0},
            PINCH={MB="LMB", MODS="", KEYCODE=0},
            DRAG={MB="LMB", MODS="", KEYCODE=0},
            SELECT={MB="LMB", MODS="", KEYCODE=0},
            ADD_SELECT={MB="LMB", MODS="Ctrl", KEYCODE=0},
            DESELECT={MB="LMB", MODS="Alt", KEYCODE=0},
            ADD_SELECT_SHORT_PATH={MB="LMB", MODS="Shift", KEYCODE=0},
            SELECT_LOOP_PATH={MB="DLMB", MODS="", KEYCODE=0},
            ADD_SELECT_LOOP_PATH={MB="DLMB", MODS="Ctrl", KEYCODE=0},
            DESELECT_PATH={MB="DLMB", MODS="Alt", KEYCODE=0},
            SELECT_TRANSLATE={MB="MMB", MODS="", KEYCODE=32},
            SELECT_ROTATE={MB="RMB", MODS="", KEYCODE=32},
            SELECT_SCALE={MB="LMB", MODS="", KEYCODE=32},
            ADD_SELECT_TRANSLATE={MB="MMB", MODS="Ctrl", KEYCODE=32},
            ADD_SELECT_ROTATE={MB="RMB", MODS="Ctrl", KEYCODE=32},
            ADD_SELECT_SCALE={MB="LMB", MODS="Ctrl", KEYCODE=32},
            TRANSLATE_ISLAND={MB="MMB", MODS="", KEYCODE=68},
            ROTATE_ISLAND={MB="RMB", MODS="", KEYCODE=68},
            SCALE_ISLAND={MB="LMB", MODS="", KEYCODE=68},
            PREVIEW_SHORT_PATH={MB="", MODS="Shift", KEYCODE=0}}})
            ZomSavePreferences(none)
        """
    )
    script: bpy.props.EnumProperty(
        name="Auto UVs",
        items=(items.get_scripts),
        description=utility.get_json("prefs", "script"),
    )

    stretch: bpy.props.FloatProperty(
        name="Stretch Control",
        default=0.0,
        min=0.0,
        max=0.99,
        description=utility.get_json("prefs", "stretch"),
    )

    sharp_value: bpy.props.IntProperty(
        name="Edge Angle",
        default=30,
        max=180,
        min=0,
        subtype="ANGLE",
        description=utility.get_json("prefs", "sharpvalue"),
    )

    mosaic_value: bpy.props.FloatProperty(
        name="Segments",
        default=0.75,
        max=0.99,
        min=0.0,
        description=utility.get_json("prefs", "mosaicvalue"),
    )

    handles: bpy.props.BoolProperty(
        name="Handles Cutter",
        default=True,
        description=utility.get_json("prefs", "handles"),
    )

    holes: bpy.props.BoolProperty(name="Holes Cutter", default=False, description=utility.get_json("prefs", "holes"))

    cylinders: bpy.props.BoolProperty(
        name="Cylinder Cutter",
        default=True,
        description=utility.get_json("prefs", "cylinders"),
    )

    leaf: bpy.props.BoolProperty(name="Leaf", default=False, description=utility.get_json("prefs", "leaf"))

    branch: bpy.props.BoolProperty(name="Branch", default=False, description=utility.get_json("prefs", "branch"))

    trunk: bpy.props.BoolProperty(name="Trunk", default=False, description=utility.get_json("prefs", "trunk"))

    # Rizom settings
    margin: bpy.props.FloatProperty(
        name="Margin",
        default=8,
        min=0,
        subtype="PIXEL",
        soft_max=32,
        description=utility.get_json("prefs", "margin"),
    )

    spacing: bpy.props.FloatProperty(
        name="Spacing",
        default=16,
        min=0,
        subtype="PIXEL",
        soft_max=32,
        description=utility.get_json("prefs", "spacing"),
    )

    tex_density: bpy.props.FloatProperty(
        name="Texel Density",
        default=10.24,
        min=0,
        subtype="PIXEL",
        description=utility.get_json("prefs", "tex_density"),
    )

    tex_units: bpy.props.EnumProperty(
        name="Texel Density Unit",
        items=(
            ("tx/km", "tx/km", ""),
            ("tx/m", "tx/m", ""),
            ("tx/dm", "tx/dm", ""),
            ("tx/cm", "tx/cm", ""),
            ("tx/mm", "tx/mm", ""),
            ("tx/in", "tx/in", ""),
            ("tx/ft", "tx/ft", ""),
            ("tx/yd", "tx/yd", ""),
            ("tx/mi", "tx/mi", ""),
        ),
        default="tx/cm",
        description=utility.get_json("prefs", "tex_unit"),
    )

    map_res: bpy.props.IntProperty(
        name="Map Resolution",
        default=2048,
        min=0,
        subtype="PIXEL",
        description=utility.get_json("prefs", "mapres"),
    )

    image_path: bpy.props.StringProperty(
        name="",
        subtype="FILE_PATH",
        default="Texture Image (optional)",
        description=utility.get_json("prefs", "image"),
    )

    init_orient: bpy.props.EnumProperty(
        name="",
        default="1",
        items=(
            ("0", "No Pre-Orientation", "Do not pre-orient islands"),
            ("1", "Horizontal Pre-Orientation", "Pre-orient islands horizontally"),
            ("2", "Vertical Pre-Orientation", "Pre-orient islands vertically"),
            ("3", "X Pre-Orientation", "Pre-orient islands on X-axis"),
            ("4", "Y Pre-Orientation", "Pre-orient islands Y-axis"),
            ("5", "Z Pre-Orientation", "Pre-orient islands Z-axis"),
        ),
        description=utility.get_json("prefs", "preorient"),
    )

    orient_step: bpy.props.IntProperty(
        name="Step Angle",
        default=90,
        step=90,
        min=0,
        max=180,
        subtype="ANGLE",
        description=utility.get_json("prefs", "orientstep"),
    )

    mutations: bpy.props.IntProperty(
        name="Mutations",
        default=1,
        max=1000,
        min=0,
        description=utility.get_json("prefs", "mutations"),
    )

    pack_qual: bpy.props.IntProperty(
        name="Quality",
        default=512,
        max=2048,
        min=0,
        description=utility.get_json("prefs", "packqual"),
    )



    tflip: bpy.props.BoolProperty(name="T Flips", default=True, description=utility.get_json("prefs", "tflip"))

    overlap: bpy.props.BoolProperty(name="Overlaps", default=True, description=utility.get_json("prefs", "overlap"))

