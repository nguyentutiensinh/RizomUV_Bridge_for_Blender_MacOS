uvmaps = ZomGet("Lib.UVSets")

for i,uvmap in pairs(map_list) do
	ZomUvset({Mode="Create", Name=uvmap})
    ZomUvset({Mode = "SetCurrent", Name=uvmap})
    ZomResetTo3d({WorkingSet="Visible", Rescale=true})
end