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
                else:
                    walls.append(obj)
            
            if walls:
                for wall in walls:
                    for opening in openings:
                        model.create_entity("IfcRelVoidsElement",
                                             RelatingBuildingElement=wall,
                                             RelatedOpeningElement=opening
                        )

        return {"FINISHED"}
    
