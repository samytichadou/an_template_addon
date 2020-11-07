import bpy
import os

from .addon_prefs import get_addon_preferences
from .global_variables import newsfeed_file, newsfeed_url
from .internet_functions import download_file
from .json_functions import read_json, load_json_in_collection
from .print_functions import print_and_report


# download newsfeed file if needed
def download_newsfeed(manifest_dataset):
    newsfeed_path = os.path.join(get_addon_preferences().download_folder, newsfeed_file)

    if not os.path.isfile(newsfeed_path):
        download_file(newsfeed_url, newsfeed_path)
        print_and_report(None, "Downloading Newsfeed", "INFO") #debug
        return True
    
    elif manifest_dataset["newsfeed_hash"] != read_json(newsfeed_path)["newsfeed_hash"]:
        download_file(newsfeed_url, newsfeed_path)
        print_and_report(None, "Downloading Newsfeed", "INFO") #debug
        return True

    return False


# reload newsfeed datas
def reload_newsfeed():

    print_and_report(None, "Loading Newsfeed", "INFO") #debug

    newsfeed_path = os.path.join(get_addon_preferences().download_folder, newsfeed_file)

    properties_coll = bpy.data.window_managers[0].an_templates_properties

    load_json_in_collection(read_json(newsfeed_path), properties_coll.news, 'news')