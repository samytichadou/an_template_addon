import bpy
import os


from .addon_prefs import get_addon_preferences
from .global_variables import addon_print_prefix, manifest_file
from .file_functions import create_directory
from .internet_functions import is_connected, download_file, read_manifest
from .json_functions import set_nodetrees_from_json, set_properties_from_json, read_json


# load manifest function
def load_manifest():

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
        return False

    print(addon_print_prefix + "Loading Manifest") #debug
    set_nodetrees_from_json(manifest_dataset)
    set_properties_from_json(manifest_dataset)

    print(addon_print_prefix + "Manifest Successfully Loaded") #debug

    return True


class ANTEMPLATES_OT_refresh_templates(bpy.types.Operator):
    """Refresh Template List From Internet"""
    bl_idname = "antemplates.refresh_templates"
    bl_label = "Refresh Templates"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        manifest_dataset = read_manifest(get_addon_preferences().manifest_url)

        if manifest_dataset["manifest_hash"] == context.window_manager.an_templates_properties.manifest_hash:
            print(addon_print_prefix + "Manifest Up to Date, Aborting")

        else:

            load_manifest()

        return {'FINISHED'}