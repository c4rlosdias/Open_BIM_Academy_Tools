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
        objs_to_be_voided = []
        allowed_types = ["IfcWall", "IfcCovering"]
        objs = [tool.Ifc.get_entity(o) for o in context.selected_objects 
                if tool.Ifc.get_entity(o).is_a() in allowed_types]
        if objs:
            for obj in objs:
                rels = obj.HasOpenings
                if rels:
                    for rel in rels:
                        openings.append(rel.RelatedOpeningElement)
                else:
                    objs_to_be_voided.append(obj)
            
            if objs_to_be_voided:
                for wall in objs_to_be_voided:
                    for opening in openings:
                        model.create_entity("IfcRelVoidsElement",
                                             RelatingBuildingElement=wall,
                                             RelatedOpeningElement=opening
                        )

        return {"FINISHED"}
    
