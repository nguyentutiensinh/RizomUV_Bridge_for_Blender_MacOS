from bpy.types import Operator

class OP_FixUVMaps(Operator):
    bl_description = 'Makes sure all selected objects have the same UV maps as the active object.\nFix invalid UV names and create new UV maps if none exist.\n(WILL OVERWRITE ANY EXISTING UV DATA)'
    bl_idname = "ruv.fix_uvmaps"
    bl_label = "Fix UV Maps"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    def execute(self, context):
        act_obj = context.active_object
        sel_objs = [obj for obj in context.selected_objects if obj.type == "MESH" and obj != act_obj]

        act_obj_map_names = [uvmap.name for uvmap in act_obj.data.uv_layers]

        if not act_obj_map_names:
            act_obj.data.uv_layers.new(name=act_obj.name, do_init=True)

        for uvmap in act_obj.data.uv_layers:
            uvmap.name = uvmap.name.replace(".", "_")

        act_obj_map_names = [uvmap.name for uvmap in act_obj.data.uv_layers]

        for obj in sel_objs:
            obj_map_names = [uvmap.name for uvmap in obj.data.uv_layers]
            if obj_map_names == act_obj_map_names:
                continue
            else:
                while obj.data.uv_layers:
                    obj.data.uv_layers.remove(obj.data.uv_layers[0])
                for name in act_obj_map_names:
                    obj.data.uv_layers.new(name=name)
        self.report({"INFO"}, "UV Maps verified")
        return {"FINISHED"}
#DEBUG', 'INFO', 'OPERATOR', 'PROPERTY', 'WARNING', 'ERROR', 'ERROR_INVALID_INPUT', 'ERROR_INVALID_CONTEXT', 'ERROR_OUT_OF_MEMORY'