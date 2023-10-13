import bpy
from bpy.types import Operator

class OP_AutoUVs(Operator):
    bl_idname = "ruv.rizom_auto"
    bl_label = "Automatic UVs"
    bl_description = "Automatically create UVs for the selected objects"
    bl_options = {"REGISTER", "INTERNAL"}
    @classmethod
    def poll(cls, context):

        props = context.preferences.addons["RUV"].preferences

        return context.active_object is not None and props.script not in ("NO_SCRIPT", "FLATTEN")

    def execute(self, context):  # pylint: disable=unused-argument
        props = context.preferences.addons["RUV"].preferences
        self.report({"INFO"}, props.lua_path)
        try:
            bpy.ops.ruv.exp(communicate=True)
        except (OSError, FileNotFoundError, RuntimeError):
            self.report({"ERROR"}, "Operation failed, please check the system console for more information")
            return {"CANCELLED"}

        bpy.ops.ruv.imp()

        self.report({"INFO"}, "UV map generated")

        return {"FINISHED"}
