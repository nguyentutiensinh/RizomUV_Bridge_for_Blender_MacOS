bl_info = {
    "name": "RizomUV Bridge MacOS",
    "author": "nguyendinhat",
    "version": (1, 2),
    "blender": (3, 6, 3),
    "location": "View3D > Sidebar",
    "description": "Addon Connect Blender with RizomUV",
    "doc_url": "https://github.com/nguyendinhat/RizomUV_Bridge_for_Blender",
    "category": "UV",
}

import bpy

from .context import addon, context
from .operators import export_uv, import_uv, auto_uv, fixuvmap, load_recent, close_rizom, reset
from .interface import View3D

RUV_PROCESS = None

CLASSES = [
    export_uv.OP_EXP,
    import_uv.OP_IMP,
    load_recent.OP_LoadRecent,
    close_rizom.OP_CloseRizom,
    addon.RUV_AddonPreferences,
    context.RUV_Context,
    View3D.RUV_Panel,
    fixuvmap.OP_FixUVMaps,
    auto_uv.OP_AutoUVs,
    reset.OP_ResetAddon,
    reset.OP_ResetConfigRizom,
]

def register():

    for cls in CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.RUV_Context = bpy.props.PointerProperty(type=context.RUV_Context)

def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.RUV_Context

if __name__ == "__main__":
    bpy.utils.register()