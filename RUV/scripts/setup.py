import bpy,os

def convert_td(tex_den, unit):

    unit_dic = {
        "tx/km": tex_den,
        "tx/m": tex_den,
        "tx/dm": tex_den * 10,
        "tx/cm": tex_den * 100,
        "tx/mm": tex_den * 1000,
        "tx/in": tex_den * 39.37,
        "tx/ft": tex_den / 0.3048,
        "tx/yd": tex_den * 1.093613,
        "tx/mi": tex_den * 0.000621371,
    }

    output = unit_dic[unit]

    return output


class ScriptSetup:
    def __init__(self, context, target_map, map_list=[]):
        self.prefs = bpy.context.preferences.addons["RUV"].preferences
        self.context = context
        self.target_map = target_map
        self.map_list = map_list
        self.file_path = self.prefs.temp_path.replace(os.sep, "/")
        self.scripts_dic = {
            "FLATTEN": self.prefs.lua_path + "flatten.lua",
            "SHARP_EDGES": self.prefs.lua_path + "sharp_edge_algorithm.lua",
            "MOSAIC": self.prefs.lua_path + "mosaic_algorithm.lua",
            "PELT": self.prefs.lua_path + "pelt_algorithm.lua",
            "BOX": self.prefs.lua_path + "box_algorithm.lua",
            "SETTINGS": self.prefs.lua_path + "settings.lua",
            "CONSTRUCT": self.prefs.lua_path + "final_script.lua",
        }

        self.file_path = self.prefs.temp_path.replace(os.sep, "/")
        self.props =  context.window_manager.RUV_Context


    def base_script(self, script):

        suffix = 'ZomSet({Path = "Prefs.FileSuffix", Value = ""})'
        uv_order = 'ZomSet({Path = "Prefs.File.FBX.UseUVSetNames", Value = true})'

        colorMap = 'ZomSet({Path="Vars.Viewport.ColorMapIDDisplayMode", Value=1})'

        displayMode = """
            ZomSet({Path="Prefs.UI.Display.MultiUVSet", Value=false})
            ZomSet({Path="Prefs.UI.Display.AlignStraightenFlip", Value=true})
            ZomSet({Path="Prefs.UI.Display.AutoSelect", Value=true})
            ZomSet({Path="Prefs.UI.Display.Help", Value=false})
            ZomSet({Path="Prefs.UI.Display.Seams", Value=false})
            ZomSet({Path="Prefs.UI.Display.ScriptLog", Value=false})
            ZomSet({Path="Prefs.UI.Display.PackLayout", Value=true})
            ZomSet({Path="Prefs.UI.Display.UnfoldOptimize", Value=true})
            ZomSet({Path="Prefs.UI.Display.Transform", Value=false})
            ZomSet({Path="Prefs.UI.Display.Proportional", Value=false})
            ZomSet({Path="Prefs.UI.Display.Grid", Value=false})
            ZomSet({Path="Prefs.UI.Display.TileSizeOffset", Value=false})
            ZomSet({Path="Prefs.UI.Display.MultiTile", Value=false})
        """

        packingMode = """
            ZomSet({Path="Prefs.Default.Packing.MinScaling", Value=0})
            ZomSet({Path="Prefs.Default.Packing.MaxScaling", Value=1e+06})
            ZomSet({Path="Prefs.PackOptions.MixScales", Value=true})
        """


        if self.prefs.script == "FLATTEN":
            mesh_load = f'ZomLoad({{File={{Path="{self.file_path}", ImportGroups=true, XYZ=true}}, NormalizeUVW=true, __UpdateGUIFilePath=true, __Focus=true}})'

        else:
            mesh_load = f'ZomLoad({{File={{Path="{self.file_path}", ImportGroups=true, XYZUVW=true, UVWProps=true}}, __UpdateGUIFilePath=true, __Focus=true}})'

        script.write("\n" + suffix + "\n" + uv_order + "\n" + "\n" +colorMap + "\n" +displayMode + "\n" +packingMode + "\n" + "\n" + mesh_load)

    def set_variables(self, script):

        valid_extensions = (".tiff", ".png", ".jpg", ".tga", ".bmp")

        if self.prefs.image_path.lower().endswith(valid_extensions):
            image_path_var = str(self.prefs.image_path).lower().replace(os.sep, "/")
            image_path = f'image_path = "{image_path_var}"'
        else:
            image_path = ""

        # These variables depend on Rizom build version, included for backwards compatibility.
        tex_density_var = None
        tex_unit = None

        tex_unit = self.prefs.tex_units
        tex_density_var = convert_td(self.prefs.tex_density, tex_unit)

        map_list = str(self.map_list).replace("[", "{", 1).replace("]", "}", -1)

        primary_vars = [f'target_map = "{self.target_map}"', f"map_list = {map_list}"]

        secondary_vars = [
            f"branch = {str(self.prefs.branch).lower()}",
            f"cylinders = {str(self.prefs.cylinders).lower()}",
            f"handles = {str(self.prefs.handles).lower()}",
            f"holes ={str(self.prefs.holes).lower()}",
            f"init_orient = {self.prefs.init_orient}",
            f"leaf = {str(self.prefs.leaf).lower()}",
            f"map_res = {self.prefs.map_res}",
            f"mosaic_value = {self.prefs.mosaic_value}",
            f"mutations = {self.prefs.mutations}",
            f"orient_step = {self.prefs.orient_step}",
            f"overlap = {str(self.prefs.overlap).lower()}",
            f"pack_qual = {self.prefs.pack_qual}",
            f"margin = {self.prefs.margin / self.prefs.map_res}",
            f"spacing = {self.prefs.spacing / self.prefs.map_res}",
            f"sharp_value = {self.prefs.sharp_value}",
            f"stretch = {self.prefs.stretch}",
            f"tex_density = {tex_density_var}",
            f'tex_unit = "{tex_unit}"',
            f"tflip = {str(self.prefs.tflip).lower()}",
            f"trunk = {str(self.prefs.trunk).lower()}",
            image_path,
        ]

        for var in primary_vars:
            script.write("\n" + var)

        if self.prefs.settings:
            for var in secondary_vars:
                script.write("\n" + var)

    def preset_script(self, script):
        key = self.prefs.script

        if key == "NO_SCRIPT":
            return

        preset = self.scripts_dic[key]

        lua_file = open(preset, "r", encoding="utf-8")
        lua_file_code = lua_file.read()
        lua_file.close()

        script.write("\n" + lua_file_code)

    def settings(self, script):

        lua_file = open(self.scripts_dic["SETTINGS"], "r", encoding="utf-8")
        lua_file_code = lua_file.read()
        lua_file.close()

        script.write("\n" + lua_file_code)

    def save_file(self, script):
        file_save = f'ZomSave({{File={{Path="{self.file_path}", UVWProps=true, FBX={{UseUVSetNames=true}}}}, __UpdateUIObjFileName=true}})'
        script.write("\n" + file_save)

    def construct_quit_app(self, truncate):
        script = open(self.scripts_dic["CONSTRUCT"], "a", encoding="utf-8")
        if truncate:
            script.truncate(0)
        self.save_file(script)
        script.write("\n" + "ZomQuit()")
        script.close()

    def construct_load_recent(self):
        """Write and execute the LUA script to load the most recent file in RizomUV."""

        final_script = open(self.scripts_dic["CONSTRUCT"], "w", encoding="utf-8")
        final_script.truncate(0)

        self.base_script(final_script)

        if self.prefs.settings:
            self.settings(final_script)

        self.save_file(final_script)
        final_script.close()

    def construct_main_script(self):

        final_script = open(self.scripts_dic["CONSTRUCT"], "w", encoding="utf-8")
        final_script.truncate(0)

        self.base_script(final_script)
        self.set_variables(final_script)

        if self.prefs.settings:
            self.settings(final_script)

        if self.prefs.script == "FLATTEN":
            self.preset_script(final_script)


        set_map = f'ZomUvset({{Mode="SetCurrent", Name="{self.target_map}"}})'
        final_script.write("\n" + set_map)

        if self.prefs.script not in ("NO_SCRIPT", "FLATTEN"):
            self.preset_script(final_script)

        self.save_file(final_script)

        final_script.close()
        return final_script

