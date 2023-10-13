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
