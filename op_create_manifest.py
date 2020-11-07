import bpy
import os
import string
import random


from .json_functions import read_json, create_json_file
from .global_variables import nodetree_infos, global_k_filepath, global_k_url, global_k_file, newsfeed_file
from .addon_prefs import get_addon_preferences
from .print_functions import print_and_report
from .internet_functions import download_file


# return direct subfolders
def return_direct_subfolders(folderpath):

    folder_paths = []

    for item in os.listdir(folderpath):

        item_path = os.path.join(folderpath, item)

        if os.path.isdir(item_path):
            folder_paths.append(item_path)

    return sorted(folder_paths)


# return direct files in folder
def return_direct_files(folderpath):

    file_paths = []

    for item in os.listdir(folderpath):

        item_path = os.path.join(folderpath, item)

        if os.path.isfile(item_path):
            file_paths.append(item_path)

    return file_paths


# generate hash number
def generate_hash(length):
    
    letters = string.ascii_letters
    digits = string.digits
    
    rd_string = "".join(random.choice(letters + digits) for i in range(length))

    return rd_string


# get k_time
def get_global_k():
    if not os.path.isfile(global_k_filepath):
        return None
    datas = read_json(global_k_filepath)
    return datas["k"], datas["w"], datas["v"]


# initialize json manifest datas
def initialize_json_manifest_datas():

    datas = {}

    datas["nodetrees"] = []
    datas["blender_versions"] = []
    datas["an_versions"] = []
    datas["categories"] = []
    datas["tags"] = []
    datas["manifest_hash"] = generate_hash(10)
    datas["k_v"] = ""
    datas["newsfeed_hash"] = ""

    return datas


# get separated tags
def get_separated_tags(tag_line):
    tags = []
    if tag_line != "":
        for t in tag_line.split(","):
            tags.append(t.strip())
    return tags


# get k_v from folder
def get_k_v(folder):
    k_v_filepath = os.path.join(folder, global_k_file)
    if os.path.isfile(k_v_filepath):
        return read_json(k_v_filepath)["v"]
    else:
        return None


# get newsfeed_v from folder
def get_newsfeed_hash(folder):
    newsfeed_hash_filepath = os.path.join(folder, newsfeed_file)
    if os.path.isfile(newsfeed_hash_filepath):
        return read_json(newsfeed_hash_filepath)["newsfeed_hash"]
    else:
        return None


class ANTEMPLATES_OT_create_manifest(bpy.types.Operator):
    """Create Manifest from Github URL and Template Folder"""
    bl_idname = "antemplates.create_manifest"
    bl_label = "Create Manifest"
    bl_options = {'REGISTER', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        prefs = get_addon_preferences()
        if os.path.isdir(bpy.path.abspath(prefs.template_folder)):
            return prefs.output_manifest_file != ""


    def execute(self, context):

        prefs = get_addon_preferences()
        
        # check and correct output path

        json_path = bpy.path.abspath(prefs.output_manifest_file)

        template_folder = bpy.path.abspath(prefs.template_folder)

        if not os.path.isdir(os.path.dirname(json_path)):
            print_and_report(self, "Incorrect Output Path", "WARNING") #debug
            return {'FINISHED'}

        if not os.path.isdir(template_folder):
            print_and_report(self, "Incorrect Template Folder Path", "WARNING") #debug
            return {'FINISHED'}

        if not json_path.endswith(".json"):
            json_path += ".json"

        # create manifest datas

        tag_list = []

        manifest_datas = initialize_json_manifest_datas()

        # set k_v and newsfeed_v

        k_v = get_k_v(template_folder)
        if k_v is not None:
            manifest_datas["k_v"] = k_v
        else:
            print_and_report(None, "No global_k file found", "WARNING") #debug

        newsfeed_hash = get_newsfeed_hash(template_folder)
        if newsfeed_hash is not None:
            manifest_datas["newsfeed_hash"] = newsfeed_hash
        else:
            print_and_report(None, "No newsfeed file found", "WARNING") #debug

        
        for folder in return_direct_subfolders(template_folder):

            # get categories
            category = os.path.basename(folder)
            manifest_datas["categories"].append(category)

            # get nodetrees
            for subfolder in return_direct_subfolders(folder):
                
                for filepath in return_direct_files(subfolder):

                    if os.path.basename(filepath) == nodetree_infos:

                        nodetree_datas = read_json(filepath)

                        # create json entry for the nodetree
                        nodetree_datas["category"] = category
                        manifest_datas["nodetrees"].append(nodetree_datas)

                        for tag in get_separated_tags(nodetree_datas["tags"]):
                            if tag not in tag_list:
                                tag_list.append(tag)

                        if nodetree_datas["blender_version"] not in manifest_datas["blender_versions"]:
                            manifest_datas["blender_versions"].append(nodetree_datas["blender_version"])

                        if nodetree_datas["an_version"] not in manifest_datas["an_versions"]:
                            manifest_datas["an_versions"].append(nodetree_datas["an_version"])

                        break

        manifest_datas["tags"] = sorted(tag_list)

        print_and_report(None, "Creating Manifest : %s" % json_path, "INFO") #debug

        #print(manifest_datas) #debug

        create_json_file(manifest_datas, json_path)

        print_and_report(self, "Manifest Successfully Created", "INFO") #debug

        return {'FINISHED'}