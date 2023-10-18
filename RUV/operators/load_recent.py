import os, bpy
from bpy.types import Operator
from ..scripts import setup
from ..operators import utility


class OP_LoadRecent(Operator):

    bl_description = "Load the most recent file in RizomUV"
    bl_idname = "ruv.rizom_recent"
    bl_label = "Load Recent"
    bl_options = {"REGISTER", "INTERNAL"}


    global RUV_PROCESS

    @classmethod
    def poll(self, context):  # pylint: disable=unused-argument
        prefs = bpy.context.preferences.addons["RUV"].preferences

        return os.path.isfile(prefs.temp_path)

    def execute(self, context):
        prefs = context.preferences.addons["RUV"].preferences

        final_script = setup.ScriptSetup(context, None).construct_load_recent()

        try:
            ppoll = self.RUV_PROCESS.poll()
        except AttributeError:
            ppoll = True

        if ppoll is not None:
            try:
                utility.open_rizom(self,context, prefs.rizom_path,prefs.temp_path, False, final_script)
            except (OSError, FileNotFoundError):
                self.report({"ERROR"}, utility.get_json("errors", "noexe"))


        return {"FINISHED"}