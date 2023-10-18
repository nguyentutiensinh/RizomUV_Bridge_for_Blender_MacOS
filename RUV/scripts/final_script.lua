
ZomSet({Path = "Prefs.FileSuffix", Value = ""})
ZomSet({Path = "Prefs.File.FBX.UseUVSetNames", Value = true})

ZomSet({Path="Vars.Viewport.ColorMapIDDisplayMode", Value=1})

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
        

            ZomSet({Path="Prefs.Default.Packing.MinScaling", Value=0})
            ZomSet({Path="Prefs.Default.Packing.MaxScaling", Value=1e+06})
            ZomSet({Path="Prefs.PackOptions.MixScales", Value=true})
        
ZomSet({Path="Prefs.CustomMousePreset", Value={ORBIT={MB="MMB", MODS="", KEYCODE=0}, ZOOM={MB="MMB", MODS="Alt-Ctrl", KEYCODE=0}, PAN={MB="MMB", MODS="Shift", KEYCODE=0}, DENSITY_PAINT={MB="LMB", MODS="", KEYCODE=0}, OPTIMIZE_PAINT={MB="LMB", MODS="", KEYCODE=0}, PIN_PAINT={MB="LMB", MODS="", KEYCODE=0}, PROTECT_PAINT={MB="LMB", MODS="", KEYCODE=0}, UNFOLD_PAINT={MB="LMB", MODS="", KEYCODE=0}, SPREAD={MB="LMB", MODS="", KEYCODE=0}, PINCH={MB="LMB", MODS="", KEYCODE=0}, DRAG={MB="LMB", MODS="", KEYCODE=0}, SELECT={MB="LMB", MODS="", KEYCODE=0}, ADD_SELECT={MB="LMB", MODS="Ctrl", KEYCODE=0}, DESELECT={MB="LMB", MODS="Alt", KEYCODE=0}, ADD_SELECT_SHORT_PATH={MB="LMB", MODS="Shift", KEYCODE=0}, SELECT_LOOP_PATH={MB="DLMB", MODS="", KEYCODE=0}, ADD_SELECT_LOOP_PATH={MB="DLMB", MODS="Ctrl", KEYCODE=0}, DESELECT_PATH={MB="DLMB", MODS="Alt", KEYCODE=0}, SELECT_TRANSLATE={MB="MMB", MODS="", KEYCODE=32}, SELECT_ROTATE={MB="RMB", MODS="", KEYCODE=32}, SELECT_SCALE={MB="LMB", MODS="", KEYCODE=32}, ADD_SELECT_TRANSLATE={MB="MMB", MODS="Ctrl", KEYCODE=32}, ADD_SELECT_ROTATE={MB="RMB", MODS="Ctrl", KEYCODE=32}, ADD_SELECT_SCALE={MB="LMB", MODS="Ctrl", KEYCODE=32}, TRANSLATE_ISLAND={MB="MMB", MODS="", KEYCODE=68}, ROTATE_ISLAND={MB="RMB", MODS="", KEYCODE=68}, SCALE_ISLAND={MB="LMB", MODS="", KEYCODE=68}, PREVIEW_SHORT_PATH={MB="", MODS="Shift", KEYCODE=0}}})ZomSet({Path="Prefs.MousePresetMode", Value=11})
ZomLoad({File={Path="/var/folders/jf/pqnw30vs0wv45kz43ft65bn80000gn/T/export_temp.fbx", ImportGroups=true, XYZUVW=true, UVWProps=true}, __UpdateGUIFilePath=true, __Focus=true})
target_map = "UVMap"
map_list = {'UVMap'}
branch = false
cylinders = true
handles = true
holes =false
init_orient = 1
leaf = false
map_res = 2048
mosaic_value = 0.75
mutations = 1
orient_step = 90
overlap = true
pack_qual = 512
margin = 0.00390625
spacing = 0.0078125
sharp_value = 30
stretch = 0.0
tex_density = 1023.9999771118164
tex_unit = "tx/cm"
tflip = true
trunk = false

-- settings.lua

if type(map_list) == "table" then
    for _, x in pairs(map_list) do
        ZomUvset({Mode = "SetCurrent", Name = x})

        ZomIslandGroups({
            Mode = "SetGroupsProperties",
            WorkingSet = "Visible",
            MergingPolicyString = "A_ADD|AIB_ADD_A_VALUE_B|B_CLONE",
            GroupPath = "RootGroup",
            Properties = {
                Pack = {
                    Scaling = {TexelDensity = tex_density},
                    MapResolution = map_res,
                    MarginSize = margin,
                    PaddingSize = spacing,
                    Rotate = {Step = orient_step, Mode = init_orient},
                    MaxMutations = mutations,
                    Resolution = pack_qual
                }
            }
        })
        -- prevent tflips/overlaps
        ZomSet({Path = "Prefs.TriangleFlipsOn", Value = tflip})
        ZomSet({Path = "Prefs.OverlapsOn", Value = overlap})
    end
end


stretch = ZomGet("Vars.AutoSelect.BijectiverMinQ")
holes = ZomGet("Vars.AutoSelect.LinkHoles")
handles = ZomGet("Vars.AutoSelect.CutHandles")
mosaic_value = ZomGet("Vars.AutoSelect.Mosaic.Developability")
sharp_value = ZomGet("Vars.AutoSelect.SharpEdges.Angle")

leaf = ZomGet("Vars.AutoSelect.Hierarchical.Leafs")
branch = ZomGet("Vars.AutoSelect.Hierarchical.Branches")
trunk = ZomGet("Vars.AutoSelect.Hierarchical.Trunk")

stretch_bool = ZomGet("Vars.AutoSelect.Bijectiver")
-- stretch control (autoseams)
if stretch > 0 then
    ZomSet({Path = "Vars.AutoSelect.Bijectiver", Value = true})
else
    ZomSet({Path = "Vars.AutoSelect.Bijectiver", Value = false})
end

ZomSet({Path = "Vars.AutoSelect.BijectiverMinQ", Value = stretch})

-- sharp edge angle (autoseams)
ZomSet({Path = "Vars.AutoSelect.SharpEdges.Angle", Value = sharp_value})

-- mosaic value (autoseams)
ZomSet({Path = "Vars.AutoSelect.Mosaic.Developability", Value = mosaic_value})

-- cut handles/cut holes (autoseams)
ZomSet({Path = "Vars.AutoSelect.CutHandles", Value = handles})
ZomSet({Path = "Vars.AutoSelect.LinkHoles", Value = holes})
ZomSet({Path = "Vars.AutoSelect.OpenCylinders", Value = cylinders})

-- leaf/branch/trunk (autoseams)
ZomSet({Path = "Vars.AutoSelect.Hierarchical.Leafs", Value = leaf})
ZomSet({Path = "Vars.AutoSelect.Hierarchical.Branches", Value = branch})
ZomSet({Path = "Vars.AutoSelect.Hierarchical.Trunk", Value = trunk})

-- image_path
if image_path then
    ZomLoadUserTexture(image_path)
    ZomSet({Path = "Vars.Viewport.Viewport3D.Textured", Value = true})
    ZomSet({Path = "Vars.Viewport.TextureID", Value = 2})
    ZomSet({Path = "Vars.Viewport.BackGroundTextureOn", Value = true})
    ZomSet({Path = "Vars.Viewport.ViewportUV.Textured", Value = true})
    ZomSet({Path = "Vars.Viewport.TextureID", Value = 2})
    ZomSet({Path = "Vars.Viewport.ColorMapIDDisplayMode", Value = 0})
end



if leaf then
    leaf = 1
else
    leaf = 0
end

if branch then
    branch = 2
else
    branch = 0
end

if trunk then
    trunk = 3
else
    trunk = 0
end

ZomUvset({Mode="SetCurrent", Name="UVMap"})
ZomSave({File={Path="/var/folders/jf/pqnw30vs0wv45kz43ft65bn80000gn/T/export_temp.fbx", UVWProps=true, FBX={UseUVSetNames=true}}, __UpdateUIObjFileName=true})