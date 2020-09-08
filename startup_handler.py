import bpy
import os
from bpy.app.handlers import persistent


from .internet_functions import read_manifest, is_connected, download_file
from .json_functions import set_nodetrees_from_json, set_properties_from_json, read_json
from .addon_prefs import get_addon_preferences
from .global_variables import addon_print_prefix, manifest_file
from .file_functions import create_directory


### HANDLER ###
@persistent
def ant_startup_handler(scene):
    
    print(addon_print_prefix + "Loading") #debug

    prefs = get_addon_preferences()

    manifest_path = os.path.join(prefs.download_folder, manifest_file)

    if not os.path.isdir(prefs.download_folder):
        print(addon_print_prefix + "Creating Download Folder") #debug
        create_directory(prefs.download_folder)


    if not is_connected():

        print(addon_print_prefix + "No Internet Connection, Trying to Load Old Manifest") #debug

    else:

        print(addon_print_prefix + "Internet Connection Available") #debug

        print(addon_print_prefix + "Downloading Manifest") #debug
        download_file(prefs.manifest_url, manifest_path)

    try:

        manifest_dataset = read_json(manifest_path)

    except FileNotFoundError:

        print(addon_print_prefix + "No Existing Manifest File") #debug
        # raise error message TODO
        return

    print(addon_print_prefix + "Loading Manifest") #debug
    set_nodetrees_from_json(manifest_dataset)
    set_properties_from_json(manifest_dataset)

    print(addon_print_prefix + "Manifest Successfully Loaded") #debug