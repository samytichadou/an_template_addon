import bpy
import os
from bpy.app.handlers import persistent


from .op_refresh_templates import load_manifest
from .print_functions import print_and_report


### HANDLER ###
@persistent
def ant_startup_handler(scene):
    
    load_manifest(None)

    print_and_report(None, "Templates Successfully Loaded", "INFO") #debug