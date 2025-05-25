import bpy
from .operators import *
import bonsai.tool as tool
import textwrap



# ---------------------------------------------------------------------
# Relating void to walls
# ---------------------------------------------------------------------

class Panel_Relate_Void(bpy.types.Panel):
    
    bl_label        = "Relates void to walls"
    bl_idname       = "VIEW3D_PT_void"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "Open BIM Academy Tools"
    #bl_options      = {"DEFAULT_CLOSED"}
    
    def draw(self, context):           
        layout = self.layout
        row = layout.row()
        row.label(text="Select Walls")
        props = context.scene.my_props
        if context.selected_objects:
            objs = [tool.Ifc.get_entity(o) for o in context.selected_objects if tool.Ifc.get_entity(o).is_a("IfcWall")]            
            if objs:
                row = layout.row()
                row.label(text=f"Walls {len(objs)} found")
                row = layout.row()
                row.operator("void.relates", text="share void")


