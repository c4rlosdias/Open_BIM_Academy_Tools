import bpy
from ifctester import ids
import os
import ifcopenshell.util.element as element
import ifcopenshell.util.selector as selector
import ifcopenshell
import webbrowser
import bonsai.tool as tool



    
# ==================================================================================================
# Relate void to walls
# ==================================================================================================
class Operator_relate_void(bpy.types.Operator):
    """relates void to walls"""
    bl_idname  = "void.relates"
    bl_label   = "uri property"
    bl_options = {"REGISTER", "UNDO"}
    uri : bpy.props.StringProperty(name="uri")

    
    def execute(self, context):  
        props = context.scene.my_props
        model = tool.Ifc.get()
        openings = []
        walls = []
        objs = [tool.Ifc.get_entity(o) for o in context.selected_objects if tool.Ifc.get_entity(o).is_a("IfcWall")] 
        if objs:
            for obj in objs:
                rels = obj.HasOpenings
                if rels:
                    for rel in rels:
                        openings.append(rel.RelatedOpeningElement)
            
            for obj in objs:
                for opening in set(openings):
                    model.create_entity("IfcRelVoidsElement",
                                         RelatingBuildingElement=obj,
                                         RelatedOpeningElement=opening
                    )
                    blender_obj = tool.Ifc.get_object(obj)
                    blender_obj.select_set(True)                    
                    if obj.is_a('IfcWall'):
                        bpy.ops.bim.recalculate_wall()
                    elif obj.is_a('IfcSlab'):
                        bpy.ops.bim.recalculate_slab()
                    else:
                        bpy.ops.bim.recalculate_fill()

        return {"FINISHED"}
    
