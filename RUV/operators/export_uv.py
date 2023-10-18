import bpy
from bpy.types import Operator

from ..operators import utility
from ..scripts import setup

class OP_EXP(Operator):
    bl_idname = "ruv.exp"
    bl_label = "Export"
    bl_options = {"REGISTER", "INTERNAL"}

    communicate: bpy.props.BoolProperty(name="Communicate", default=False)
    global RUV_PROCESS

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.ops.ed.undo_push()
        prefs = bpy.context.preferences.addons["RUV"].preferences
        props = context.window_manager.RUV_Context
        active_obj = context.active_object
        selected_obj = [obj for obj in context.selected_objects if obj.type == "MESH"]

        if not selected_obj:
            selected_obj = [active_obj]

        map_list = [uvmap.name for uvmap in context.active_object.data.uv_layers]

        target_map = context.window_manager.RUV_Context.uv_maps

        if not utility.verify_objects(self,active_obj, selected_obj):
            bpy.ops.ed.undo()
            return {"CANCELLED"}
        if prefs.exclude_linked:
            clones = utility.find_clones(selected_obj)
            export_objs = [obj for obj in selected_obj if obj not in clones]
        else:
            export_objs = selected_obj

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        export_files = utility.export_file(self,export_objs)
        utility.cleanup_scene(export_files, selected_obj, active_obj)

        for obj in selected_obj:
            obj.data.uv_layers.active = obj.data.uv_layers[target_map]
        # utility.write_lua(self, prefs.luascript, props)
        final_script = setup.ScriptSetup(context, target_map, map_list).construct_main_script()
        try:
            ppoll = self.RUV_PROCESS.poll()
        except AttributeError:
            ppoll = True

        if ppoll is not None:
            try:
                utility.open_rizom(self, context,prefs.rizom_path, prefs.temp_path, self.communicate, final_script)
            except (OSError, FileNotFoundError):
                self.report({"ERROR"}, "noexe")
            if props.opt_AutoIMP == 'Y_AutoIMP':
                bpy.ops.ruv.imp()
        return {'FINISHED'}
