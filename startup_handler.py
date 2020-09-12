import bpy
import os
from bpy.app.handlers import persistent


from .op_refresh_templates import load_manifest


### HANDLER ###
@persistent
def ant_startup_handler(scene):
    
    load_manifest(None)