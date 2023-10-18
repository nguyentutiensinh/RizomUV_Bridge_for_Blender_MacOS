ZomSelect({PrimType="Edge", WorkingSet="Visible", Select=true, All=true})
ZomMove({WorkingSet="Visible", PrimType="Edge", Geometrical="TransformIslandsByEdgePairs"})
ZomWeld({PrimType="Edge", WorkingSet="Visible", Mode="All"})
ZomResetTo3d({WorkingSet="Visible", Rescale=true})

ZomSelect({PrimType="Edge", WorkingSet="Visible", Select=true, ResetBefore=true, ProtectMapName="Protect", FilterIslandVisible=true, Auto={SharpEdges={AngleMin=sharp_value}, QuasiDevelopable={Developability=0.95, IslandPolyNBMin=1, FitCones=true, Straighten=true}, PipesCutter=holes, HandleCutter=handles, QuadLoopCutter=cylinders, StretchLimiter=stretch_bool, Quality=stretch, StoreCoordsUVW=true, FlatteningMode=0, FlatteningUnfoldParams={BorderIntersections=true, TriangleFlips=true}}})
ZomCut({PrimType="Edge", WorkingSet="Visible"})
ZomLoad({Data={CoordsUVWInternalPath="#Mesh.Tmp.AutoSelect.UVW "}})
ZomIslandGroups({Mode="DistributeInTilesByBBox", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE"})
ZomIslandGroups({Mode="DistributeInTilesEvenly", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", UseTileLocks=true, UseIslandLocks=true})
ZomPack({RootGroup="RootGroup", WorkingSet="Visible", ProcessTileSelection=false, RecursionDepth=1, Translate=true, LayoutScalingMode=2, Scaling={Mode=2}})


