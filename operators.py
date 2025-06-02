import bpy
from ifctester import ids
import os
import ifcopenshell.util.element as element
import ifcopenshell.util.selector as selector
import ifcopenshell
import webbrowser
import bonsai.tool as tool


class OperatorRelateVoid(bpy.types.Operator):
    """Relate openings (voids) to selected IfcElements (excluding openings)"""
    bl_idname = "bim.relate_voids"
    bl_label = "Relate Voids to Elements"
    bl_options = {"REGISTER", "UNDO"}

    uri: bpy.props.StringProperty(name="URI")

    def execute(self, context):  
        model = tool.Ifc.get()
        selected_objects = context.selected_objects

        elements = []
        all_openings = set()

        # Collect valid elements and their openings
        for obj in selected_objects:
            entity = tool.Ifc.get_entity(obj)
            if entity and entity.is_a("IfcElement") and not entity.is_a("IfcOpeningElement"):
                elements.append(entity)
                for rel in getattr(entity, "HasOpenings", []):
                    all_openings.add(rel.RelatedOpeningElement)

        # Process each element
        for element in elements:
            if getattr(element, "FillsVoids", []):
                continue  # Skip if already filling voids

            existing_openings = {
                rel.RelatedOpeningElement for rel in getattr(element, "HasOpenings", [])
            }

            # Create missing relationships
            for opening in all_openings - existing_openings:
                model.create_entity(
                    "IfcRelVoidsElement",
                    RelatingBuildingElement=element,
                    RelatedOpeningElement=opening
                )

            # Select Blender object and recalculate geometry
            blender_obj = tool.Ifc.get_object(element)
            if blender_obj:
                blender_obj.select_set(True)

            # Determine recalculation type based on material direction
            material_direction = None
            associations = getattr(element, "HasAssociations", [])
            if associations:
                material = getattr(associations[0], "RelatingMaterial", None)
                material_direction = getattr(material, "LayerSetDirection", None)

            if material_direction == "AXIS2":
                bpy.ops.bim.recalculate_wall()
            elif material_direction == "AXIS3":
                bpy.ops.bim.recalculate_slab()
            else:
                bpy.ops.bim.recalculate_fill()

        return {"FINISHED"}

    
