import bpy
from ..operators import utility

class OP_IMP(bpy.types.Operator):
    bl_idname = "ruv.imp"
    bl_label = "Import"

    def execute(self, context):
        prefs = bpy.context.preferences.addons["RUV"].preferences
        #get obj
        active_obj = context.active_object

        #checkview
        bpy.ops.ed.undo_push()
        #change mode to OBJECT
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        #delete objs ma_rizom_tag
        for obj in bpy.data.objects:
            if "RizomUV" in obj:
                del obj["RizomUV"]
        #import file
        bpy.ops.import_scene.fbx(
            filepath = prefs.temp_path,
            axis_forward='-Z',
            axis_up='Y'
        )
        selected_obj = bpy.context.selected_objects
        if not selected_obj:
            selected_obj = [active_obj]

        rizom_objs = [obj for obj in bpy.data.objects if "RizomUV" in obj]
        matching_objs = [bpy.data.objects[obj["RizomUV"]] for obj in rizom_objs]
        for obj in rizom_objs:
            obj.name = obj["RizomUV"] + "_ruv"
        imported_objs = rizom_objs
        target_objs = matching_objs
        #collections_reveal
        layers = bpy.context.view_layer.layer_collection.children
        layers_list = [layer for layer in layers]
        for layer in layers_list:
            for child in layer.children:
                layers_list.append(child)
        obj_layers = [layer for layer in layers_list if any(obj in target_objs for obj in layer.collection.objects)]
        layer_excluded_list = [layer for layer in obj_layers if layer.exclude is True]
        layers_hidden_list = [layer for layer in obj_layers if layer.hide_viewport is True]
        for layer in layer_excluded_list:
            layer.exclude = False

        for layer in layers_hidden_list:
            layer.hide_viewport = False
        #layer_excluded_list, layers_hidden_list
        hidden_objs = [obj for obj in target_objs if not obj.visible_get()]
        for obj in hidden_objs:
            obj.hide_set(False)
        try:
            context.view_layer.objects.active = target_objs[0]
        except IndexError:
            self.report({"ERROR"}, "nomatch")
            bpy.ops.ed.undo()
            return {"CANCELLED"}
        #
        if prefs.replace:
            try:
                if prefs.seams or prefs.sharp:
                    self.mark_boundaries(prefs.seams, prefs.sharp, imported_objs)
            except RuntimeError:
                pass

            utility.cleanup_scene(target_objs, imported_objs, imported_objs[0])

        else:
            try:
                utility.uv_transfer(self,target_objs, context)
            except RuntimeError:
                for obj in imported_objs:
                    bpy.data.objects.remove(bpy.data.objects[obj.name], do_unlink=True)
                return {"CANCELLED"}

            # Purge objects and duplicated materials from FBX
            for obj in imported_objs:
                for material in obj.data.materials.items():
                    bpy.data.materials.remove(material[1])

            try:
                if prefs.seams or prefs.sharp:
                    self.mark_boundaries(prefs.seams, prefs.sharp, target_objs)
            except RuntimeError:
                pass

            utility.cleanup_scene(imported_objs, target_objs, active_obj)
        # Rehide any objects or collections that were made visible
        if not prefs.reveal:
            try:
                for layer in layer_excluded_list:
                    layer.exclude = True

                for layer in layers_hidden_list:
                    layer.hide_viewport = True
                for obj in hidden_objs:
                    obj.hide_set(True)
            except UnboundLocalError:
                pass

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.editmode_toggle()
        bpy.context.window.workspace = bpy.data.workspaces['UV Editing']
        bpy.ops.mesh.select_all(action='SELECT')


        return {'FINISHED'}
