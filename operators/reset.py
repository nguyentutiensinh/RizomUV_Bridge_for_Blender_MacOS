from bpy.types import Operator

class OP_ResetAddon(Operator):
    """Reset bridge addon settings to default values."""

    bl_description = "Reset Addon RUV settings"
    bl_idname = "ruv.bridge_config_reset"
    bl_label = "Reset all Settings"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):

        props = context.preferences.addons["RUV"].preferences

        preferences = [
            "branch",
            "cylinders",
            "handles",
            "holes",
            "leaf",
            "mosaic_value",
            "replace",
            "reveal",
            "script",
            "seams",
            "settings",
            "exclude_linked",
            "sharp_value",
            "sharp",
            "stretch",
            "trunk",
        ]

        for preference in preferences:
            props.property_unset(preference)

        self.report({"INFO"}, "\"RizomUV Bridge\" settings returned to defaults"
                    )

        return {"FINISHED"}


class OP_ResetConfigRizom(Operator):

    bl_description = "Reset Config RizomUV"
    bl_idname = "ruv.rizomuv_config_reset"
    bl_label = "Reset all RizomUV Settings"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):

        props = context.preferences.addons["RUV"].preferences

        preferences = [
            "image_path",
            "init_orient",
            "map_res",
            "margin",
            "mutations",
            "orient_step",
            "overlap",
            "pack_qual",
            "spacing",
            "tex_density",
            "tex_units",
            "tflip",
        ]

        for preference in preferences:
            props.property_unset(preference)

        self.report({"INFO"}, "\"RizomUV Settings\" settings returned to defaults")

        return {"FINISHED"}
