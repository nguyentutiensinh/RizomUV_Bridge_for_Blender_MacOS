import bpy
from bpy.types import Panel
from ..operators import export_uv, import_uv, auto_uv,fixuvmap, load_recent,close_rizom

class RUV_Panel(Panel):

    bl_idname = "PANEL_PT_RizomUVBridge"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RizomUV"
    bl_label = "RizomUV Bridge"
    spaceTypes = ['VIEW_3D', 'IMAGE_EDITOR', 'NODE_EDITOR']

    def draw(self, context):
        props = context.window_manager.RUV_Context
        prefs = bpy.context.preferences.addons["RUV"].preferences

        layout = self.layout

        box = layout.box()
        row = box.row(align=True)
        row.scale_y = 1.25
        row.scale_x = 1.25

        row.prop(props, "panel_enums", icon_only=True, expand=True)
        if props.panel_enums == "MAIN":

            row.label(text="Main")

            # Import/Export
            box = layout.box()
            row = box.row(align=True)
            row.label(text="Main Operations:", icon="UV_DATA")

            row = box.row(align=True)
            row.scale_y = 1.25
            row.operator(export_uv.OP_EXP.bl_idname, text="Export", icon="EXPORT")
            if props.opt_AutoIMP == 'N_AutoIMP':
                row.scale_y = 1.25
                row.operator(import_uv.OP_IMP.bl_idname, text="Import", icon="IMPORT")
            row = box.row(align=True)
            row.scale_y = 1.25
            row.operator(load_recent.OP_LoadRecent.bl_idname, text="Recent", icon="FILE_CACHE")
            row.scale_y = 1.25
            row.operator(close_rizom.OP_CloseRizom.bl_idname, text="Close", icon="QUIT")
            # --------------------------------------#
            # --------------------------------------#

            # Export Settings
            box = layout.box()
            row = box.row(align=True)
            row.label(text="Process:", icon="PLUGIN")
            row = box.row(align=True)
            row.scale_y = 1.25
            row.prop(props, "opt_AutoIMP")

            split = box.split()

            row = box.row(align=True)
            row.scale_y = 1.25
            row.prop(props, "uv_maps")
            row.operator(fixuvmap.OP_FixUVMaps.bl_idname, text="Fix UVSets", icon="FAKE_USER_ON")

            col = split.column(align=True)
            col.scale_y = 1.25
            if prefs.script in ("NO_SCRIPT", "FLATTEN"):
                col.enabled = False

            row = box.row(align=True)
            row.scale_y = 1.25
            row.prop(prefs, "script")
            row.operator(auto_uv.OP_AutoUVs.bl_idname, text="Run", icon="AUTO")

            #Submenu AutoSeams
            if prefs.script == "SHARP_EDGES":

                # Sharp edge value
                row = box.row(align=True)
                row.scale_y = 1.25
                row.prop(prefs, "sharp_value")
                row.prop(prefs, "stretch")

                # Link holes and cut handles options
                row = box.row(align=True)
                row.scale_y = 1.25
                row.prop(prefs, "handles", toggle=True)
                row.prop(prefs, "holes", toggle=True)
                row.prop(prefs, "cylinders", toggle=True)

            elif prefs.script == "MOSAIC":

                # Segments value
                row = box.row(align=True)
                row.scale_y = 1.25
                row.prop(prefs, "mosaic_value")
                row.prop(prefs, "stretch")

                # Link holes and cut handles options
                row = box.row(align=True)
                row.scale_y = 1.25
                row.prop(prefs, "handles", toggle=True)
                row.prop(prefs, "holes", toggle=True)
                row.prop(prefs, "cylinders", toggle=True)

            elif prefs.script == "PELT":

                row = box.row(align=True)
                row.scale_y = 1.25
                row.prop(prefs, "stretch")

                # Leaf/Branch/Trunk selections
                row = box.row(align=True)
                row.scale_y = 1.25
                row.prop(prefs, "leaf", toggle=True)
                row.prop(prefs, "branch", toggle=True)
                row.prop(prefs, "trunk", toggle=True)

                # Link holes and cut handles options
                row = box.row(align=True)
                row.scale_y = 1.25
                row.prop(prefs, "handles", toggle=True)
                row.prop(prefs, "holes", toggle=True)
                row.prop(prefs, "cylinders", toggle=True)

            elif prefs.script == "BOX":

                row = box.row(align=True)
                row.scale_y = 1.25
                row.prop(prefs, "stretch")

                # Link holes and cut handles options
                row = box.row(align=True)
                row.scale_y = 1.25
                row.prop(prefs, "handles", toggle=True)
                row.prop(prefs, "holes", toggle=True)
                row.prop(prefs, "cylinders", toggle=True)
#RUV_SETTINGS
        elif props.panel_enums == "RUV_SETTINGS":

            row.label(text="Config  ")

            box = layout.box()

            row = box.row(align=True)
            row.label(text="Viewport:", icon="VIEW3D")

            row = box.row(align=True)
            row.scale_y = 1.25
            row.prop(prefs, "image_path")

            box = layout.box()

            row = box.row(align=True)
            row.label(text="Layout:", icon="GROUP_UVS")

            row = box.row(align=True)
            row.scale_y = 1.25
            row.prop(prefs, "margin")
            row.prop(prefs, "spacing")

            row = box.row(align=True)
            row.scale_y = 1.25
            row.prop(prefs, "map_res")

            row = box.row(align=True)
            row.scale_y = 1.25
            row.prop(prefs, "tex_density")

            row.prop(prefs, "tex_units", text="")


            box = layout.box()
            row = box.row(align=True)
            row.label(text="Packing:", icon="PACKAGE")
            row = box.row(align=True)
            row.scale_y = 1.25
            row.prop(prefs, "pack_qual")
            row.prop(prefs, "mutations")
            row = box.row(align=True)
            row.scale_y = 1.25
            row.prop(prefs, "init_orient")
            row.prop(prefs, "orient_step")

            # --------------------------------------#
            # --------------------------------------#

            box = layout.box()
            row = box.row(align=True)
            row.label(text="Prevent:", icon="CANCEL")
            row = box.row(align=True)
            row.scale_y = 1.25
            row.prop(prefs, "tflip", toggle=True)
            row.prop(prefs, "overlap", toggle=True)

            box = layout.box()
            row = box.row(align=True)
            row.label(text="Reset Settings:", icon="LOOP_BACK")

            row = box.row(align=True)
            row.scale_y = 1.25
            row.operator("ruv.bridge_config_reset", text="Reset Panel")
            row.operator("ruv.rizomuv_config_reset", text="Reset config")


        elif props.panel_enums == "SETTINGS":

            row.label(text="Addon Settings")

            box = layout.box()
            row = box.row(align=True)
            row.label(text="RizomUV Path:", icon="FILEBROWSER")

            row = box.row()
            row.scale_y = 1.25
            row.prop(prefs, "rizom_path")
