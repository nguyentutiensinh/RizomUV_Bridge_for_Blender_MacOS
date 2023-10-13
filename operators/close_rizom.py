from bpy.types import Operator
from ..scripts import setup

class OP_CloseRizom(Operator):
    """Close Rizom."""

    bl_description = "Close RizomUV if it is running"
    bl_idname = "ruv.rizom_close"
    bl_label = "Close Rizom"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        setup.ScriptSetup(context, None).construct_quit_app(True)
        return {"FINISHED"}