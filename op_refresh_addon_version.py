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


# check for addon new version
def check_addon_version(self, context):

    print_and_report(None, "Checking for Addon New Version", "INFO") #debug

    if not is_connected():
            print_and_report(self, "No Internet Connection", "WARNING") #debug
            return False

    if context:
        properties_coll = context.window_manager.an_templates_properties
    else:
        properties_coll = bpy.data.window_managers[0].an_templates_properties

    new_addon_infos = read_online_json(addon_version_url)

    if new_addon_infos["version"] != get_addon_version("AN templates"):
        properties_coll.update_needed = True
        properties_coll.update_message = new_addon_infos["message"]
        properties_coll.update_download_url = new_addon_infos["download_url"]

        print_and_report(self, "New Version of the Addon Found", "INFO") #debug

        return True

    print_and_report(self, "Addon Up to Date", "INFO") #debug
    
    return False


class ANTEMPLATES_OT_refresh_addon_version(bpy.types.Operator):
    """Check for New Version of the Addon"""
    bl_idname = "antemplates.refresh_addon_version"
    bl_label = "Check Addon Version"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        check_addon_version(self, context)         

        return {'FINISHED'}