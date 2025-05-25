# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    "name"        : "Open BIM Academy Tools",
    "author"      : "Carlos Dias",
    "description" : "",
    "blender"     : (4, 3, 0),
    "version"     : (0, 0, 1),
    "location"    : "View3D > Panel > Open BIM Academy Tools",
    "warning"     : "",
    "category"    : "User"
}


import sys
import os
from bpy.props import PointerProperty
from bpy.types import Scene
from bpy.utils import register_class, unregister_class



#if sys.modules.get("bpy", None):
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "libs", "site", "packages"))

from .operators import *
from .panels import *
from .properties import *

classes = [     
    Panel_Relate_Void,
    Elements,
    Operator_relate_void,
    MyProperties,
]

def register():
    for c in classes:
        register_class(c)
    Scene.my_props = PointerProperty(type=MyProperties)


def unregister():
    del Scene.my_props
    for c in classes:
        unregister_class(c)

if __name__ == "__main__":
    register()

