import bpy
from bpy.app.handlers import persistent

from .internet_functions import read_manifest, is_connected
from .json_functions import set_nodetrees_from_json, set_properties_from_json
from .addon_prefs import get_addon_preferences


#url = r"https://raw.githubusercontent.com/samytichadou/an_template_test/master/misc_dev/test.json"

### HANDLER ###
@persistent
def antStartupHandler(scene):
    prefs = get_addon_preferences()
    
    print() #debug
    print("AN Templates") #debug
    print() #debug

    if not is_connected():
        print("No Internet connection") #debug
        # raise error message TODO
    else:
        print("Internet connection") #debug

        print("Downloading manifest") #debug
        manifest_dataset = read_manifest(prefs.manifest_url)

        print("Loading manifest") #debug
        set_nodetrees_from_json(manifest_dataset)
        set_properties_from_json(manifest_dataset)