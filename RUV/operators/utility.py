
import bpy, os, json
from ..scripts import setup
from ..operators import fixuvmap

def get_json(dictionary, key, **kwargs):

    json_dir = os.path.dirname(__file__).replace("operators", "scripts") + os.sep + "strings.json"

    with open(json_dir) as json_file:
        json_object = json.load(json_file)
        json_file.close()

    json_string = str(json_object[dictionary][key])

    return json_string

def sel_mode(vert=False, edge=False, face=False):
    mode = bpy.context.scene.tool_settings.mesh_select_mode
    if vert or edge or face:
        bpy.context.scene.tool_settings.mesh_select_mode = (vert, edge, face)
    return mode

def export_file(self, objs):
    prefs = bpy.context.preferences.addons["RUV"].preferences
    export_objs = []
    #set lastname _ruv
    for obj in objs:
        obj.name = obj.name + "_ruv"
    #copy objs in to export_objs
    for obj in objs:
        new_obj = obj.copy()
        new_obj.data = obj.data.copy()
        new_obj.name = obj.name.replace("_ruv", "")
        bpy.context.scene.collection.objects.link(new_obj)
        export_objs.append(new_obj)

    bpy.ops.object.select_all(action="DESELECT")
    # remove modifiers converpoly add attribute RizomUV
    for obj in export_objs:
        obj.select_set(True)
        obj.animation_data_clear()
        obj.modifiers.clear()
        obj["RizomUV"] = obj.name  # This is used to find the object pair for transfering UVs.
        obj.data.uv_layers.active_index = 0

    bpy.ops.export_scene.fbx(
        filepath=prefs.temp_path,
        use_selection=True,
        global_scale=1.0,
        object_types={"MESH"},
        use_mesh_edges=False,
        bake_anim=False,
        axis_forward="-Z",
        axis_up="Y",
        use_custom_props=True,
    )
    self.report({'WARNING'},"1 objects(s) FBX export as "+prefs.temp_path)
    return export_objs

def cleanup_scene(delete_objs, select_objs, active_obj):

    for obj in delete_objs:
        bpy.data.objects.remove(bpy.data.objects[obj.name], do_unlink=True)

    for obj in select_objs:
        obj.name = obj.name.replace("_ruv", "")
        obj.select_set(True)

    for mesh in bpy.data.meshes:
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)

    bpy.context.view_layer.objects.active = active_obj

def verify_objects(self, act_obj, objs):
    valid = False
    actobj_uvmap_names = [uvmap.name for uvmap in act_obj.data.uv_layers]
    # Check if any UV maps exist.
    if not actobj_uvmap_names:
        self.report({"WARNING"}, f'{act_obj.name}: No UV maps exist')
        bpy.ops.ruv.fix_uvmaps()
        actobj_uvmap_names = [uvmap.name for uvmap in act_obj.data.uv_layers]
        # return valid
    # Check that all selected objects have the same UV maps.
    for obj in objs:
        obj_uvmap_names = [uvmap.name for uvmap in obj.data.uv_layers]
        if obj_uvmap_names == actobj_uvmap_names:
            continue
        else:
            self.report({"ERROR"}, f'"{obj.name}" {("errors", "namematch")} "{act_obj.name}"')
            return valid

    # Check that object names do not exceed 59 characters (need room for _ruv suffix)
    for obj in objs:
        if len(obj.name) > 59:
            self.report({"ERROR"}, f'{("errors", "namelength")} "{obj.name}"')
            return valid
        if obj.name.endswith("_ruv"):
            self.report({"ERROR"}, f'{("errors", "namesuffix")} "{obj.name}"')
            return valid

    valid = True

    return valid

def find_clones(self, objects):


    data_blocks = []
    clones = []

    for obj in objects:
        if obj.data not in data_blocks:
            data_blocks.append(obj.data)
        else:
            clones.append(obj)

    return clones

def open_rizom(self, context,rizomPath, TEMP_PATH, communicate, final_script):
    prefs = bpy.context.preferences.addons["RUV"].preferences
    global RUV_PROCESS
    props = context.window_manager.RUV_Context
    if communicate:
        setup.ScriptSetup(context, None).construct_quit_app(False)
    if props.opt_AutoIMP == "N_AutoIMP":
        str_exec = 'open -a "' + rizomPath + '" --args "'+ TEMP_PATH +'" -cfi "'+prefs.lua_path + 'final_script.lua"'
    else:
        str_exec = 'open -W "' + rizomPath + '" --args "'+ TEMP_PATH +'" -cfi "'+prefs.lua_path + 'final_script.lua"'

    RUV_PROCESS = os.system(str_exec)
    return RUV_PROCESS





def uv_transfer(self, target_objs, context):
    report_count = (len(target_objs), len(target_objs[0].data.uv_layers))

    bpy.ops.object.select_all(action="DESELECT")

    for obj in target_objs:
        try:
            rizom_obj = bpy.data.objects[obj.name + "_ruv"]
        except KeyError:
            self.report({"ERROR"}, "nomactch"+obj.name.replace("_ruv", ""))
            raise RuntimeError

        obj.select_set(True)
        context.view_layer.objects.active = rizom_obj

        start_index = obj.data.uv_layers.active_index
        uvmap_list = target_objs[0].data.uv_layers

        if not uvmap_list:
            self.report({"ERROR"}, "nomap"+target_objs[0].name)
            raise RuntimeError
        uv_count = len(uvmap_list)
        while uv_count:
            for uvmap in uvmap_list:
                try:
                    obj.data.uv_layers.active = obj.data.uv_layers[uvmap.name]
                    rizom_obj.data.uv_layers.active = rizom_obj.data.uv_layers[uvmap.name]
                    uv_count = uv_count - 1

                except KeyError:
                    self.report({"ERROR"}, "mapmatch"+ obj.name )
                    uv_count = 0
                    raise RuntimeError

                bpy.ops.object.join_uvs()

        # Reset for next iteration
        obj.data.uv_layers.active_index = start_index
        bpy.ops.object.select_all(action="DESELECT")

    self.report({"INFO"}, f"{report_count[1]} UV map(s) updated on {report_count[0]} object(s)")

def mark_boundaries(seams, sharp, objects):

    bpy.ops.object.select_all(action="DESELECT")

    for obj in objects:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode="EDIT")
        vert, edge, face = sel_mode(False, True, False)
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.select_all(action="SELECT")
        if sharp:
            bpy.ops.mesh.mark_sharp(clear=True)
        if seams:
            bpy.ops.mesh.mark_seam(clear=True)

        bpy.ops.uv.seams_from_islands(mark_seams=seams, mark_sharp=sharp)
        bpy.ops.mesh.select_all(action="DESELECT")

        sel_mode(vert, edge, face)
        bpy.ops.object.mode_set(mode="OBJECT")