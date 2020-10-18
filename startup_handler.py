import bpy
import os
from bpy.app.handlers import persistent


from .op_refresh_templates import load_manifest
from .print_functions import print_and_report
from .op_refresh_addon_version import check_addon_version


### HANDLER ###
@persistent
def ant_startup_handler(scene):

    print_and_report(None, "Loading", "INFO") #debug
    
    internet_connection = check_addon_version(None, None)

    if load_manifest(None, internet_connection):
        print_and_report(None, "Templates Successfully Loaded", "INFO") #debug

    else:
        print_and_report(None, "Unable to Load Templates", "WARNING") #debug