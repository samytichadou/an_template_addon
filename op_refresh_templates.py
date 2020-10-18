import bpy
import os


from .addon_prefs import get_addon_preferences
from .global_variables import manifest_file, manifest_url, global_k_url, global_k_filepath, addon_version_url
from .file_functions import create_directory
from .internet_functions import is_connected, download_file, read_online_json
from .json_functions import set_nodetrees_from_json, set_properties_from_json, read_json
from .print_functions import print_and_report
from .op_create_manifest import get_global_k
from .op_submit_template import get_addon_version


# check offline available nodetrees
def check_downloaded_nodetrees():

    winman = bpy.data.window_managers[0]
    nodetrees_coll = winman.an_templates_nodetrees

    download_folder = get_addon_preferences().download_folder
    
    for item in os.listdir(download_folder):
        if item != manifest_file:
            for nt in nodetrees_coll:
                if nt.hash == item:
                    nt.downloaded = True
                    break


# load manifest function
def load_manifest(self, internet_connection):
    
    print_and_report(None, "Getting Manifest", "INFO") #debug

    prefs = get_addon_preferences()

    manifest_path = os.path.join(prefs.download_folder, manifest_file)

    if prefs.custom_library:
        specific_manifest_url = prefs.manifest_url
    else:
        specific_manifest_url = manifest_url

    if not os.path.isdir(prefs.download_folder):
        print_and_report(None, "Creating Download Folder", "INFO") #debug
        create_directory(prefs.download_folder)

    if not internet_connection:

        print_and_report(None, "No Internet Connection, Trying to Load Old Manifest", "INFO") #debug

    else:

        print_and_report(None, "Internet Connection Available", "INFO") #debug

        print_and_report(None, "Downloading Manifest", "INFO") #debug
        download_file(specific_manifest_url, manifest_path)

    try:

        manifest_dataset = read_json(manifest_path)

    except FileNotFoundError:
        print_and_report(self, "No Existing Manifest File", "WARNING") #debug
        return False

    print_and_report(None, "Loading Manifest", "INFO") #debug

    set_nodetrees_from_json(manifest_dataset)
    set_properties_from_json(manifest_dataset)

    # check available downloaded nodetrees
    print_and_report(None, "Checking Downloaded Nodetrees", "INFO") #debug
    check_downloaded_nodetrees()

    # reload k
    reload_global_k(manifest_dataset)

    return True


# load global k if needed
def reload_global_k(manifest_dataset):
    if manifest_dataset["k_v"] != get_global_k()[2]:
        print_and_report(None, "Reloading Submission System", "INFO") #debug
        download_file(global_k_url, global_k_filepath)


class ANTEMPLATES_OT_refresh_templates(bpy.types.Operator):
    """Refresh Template List From Internet"""
    bl_idname = "antemplates.refresh_templates"
    bl_label = "Refresh Templates"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        # check internet connection
        if not is_connected():
            print_and_report(self, "No Internet Connection, unable to refresh templates", "WARNING") #debug
            return {"FINISHED"}

        prefs = get_addon_preferences()

        if prefs.custom_library:
            specific_manifest_url = prefs.manifest_url
        else:
            specific_manifest_url = manifest_url

        manifest_dataset = read_online_json(specific_manifest_url)

        if manifest_dataset["manifest_hash"] == context.window_manager.an_templates_properties.manifest_hash:
            # reload global_k
            reload_global_k(manifest_dataset)
            print_and_report(self, "Manifest Up to Date", "INFO") #debug

        else:
            if load_manifest(self, is_connected()):
                print_and_report(self, "Templates Successfully Loaded", "INFO") #debug
            else:
                print_and_report(self, "Unable to Load Templates", "WARNING") #debug

        return {'FINISHED'}