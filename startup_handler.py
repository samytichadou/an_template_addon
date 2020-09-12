import bpy
import os
from bpy.app.handlers import persistent


# from .internet_functions import read_manifest, is_connected, download_file
# from .json_functions import set_nodetrees_from_json, set_properties_from_json, read_json
# from .addon_prefs import get_addon_preferences
# from .global_variables import addon_print_prefix, manifest_file
# from .file_functions import create_directory
from .op_refresh_templates import load_manifest


### HANDLER ###
@persistent
def ant_startup_handler(scene):
    
    load_manifest(None)