import bpy
from bpy.types import PropertyGroup
from bpy.props import *
import bonsai.tool as tool
import requests


class Elements(PropertyGroup):
    
    name : StringProperty(name='name')
    id   : IntProperty(name="id")


class MyProperties(PropertyGroup): 
    
    active_info_prop_index   : IntProperty(name='object index', default=0)
    active_element_index     : IntProperty(name='element index', default=0)
    elements                 : CollectionProperty(name='elements', type=Elements) 

