import bpy
from bpy.app.handlers import persistent


from .internet_functions import read_manifest, is_connected
from .json_functions import set_nodetrees_from_json, set_properties_from_json
from .addon_prefs import get_addon_preferences
from .global_variables import addon_print_prefix


### HANDLER ###
@persistent
def antStartupHandler(scene):
    prefs = get_addon_preferences()

    print(addon_print_prefix + "Loading") #debug

    if not is_connected():
        print(addon_print_prefix + "No Internet Connection") #debug
        # raise error message TODO
    else:
        print(addon_print_prefix + "Internet Connection Available") #debug

        print(addon_print_prefix + "Downloading Manifest") #debug
        manifest_dataset = read_manifest(prefs.manifest_url)

        print(addon_print_prefix + "Loading Manifest") #debug
        set_nodetrees_from_json(manifest_dataset)
        set_properties_from_json(manifest_dataset)