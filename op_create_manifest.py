import bpy
import os
import string
import random


from .json_functions import read_json, create_json_file
from .global_variables import nodetree_infos, addon_print_prefix
from .addon_prefs import get_addon_preferences


# return direct subfolders
def return_direct_subfolders(folderpath):

    folder_paths = []

    for item in os.listdir(folderpath):

        item_path = os.path.join(folderpath, item)

        if os.path.isdir(item_path):
            folder_paths.append(item_path)

    return folder_paths


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


# initialize json manifest datas
def initialize_json_manifest_datas() :

    datas = {}

    datas["nodetrees"] = []
    datas["blender_versions"] = []
    datas["an_versions"] = []
    datas["categories"] = []
    datas["manifest_hash"] = generate_hash(10)

    return datas


class ANTEMPLATES_OT_create_manifest(bpy.types.Operator):
    """Create Manifest from Github URL and Template Folder"""
    bl_idname = "antemplates.create_manifest"
    bl_label = "Create Manifest"
    bl_options = {'REGISTER', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        prefs = get_addon_preferences()
        return prefs.output_manifest_file != "" and os.path.isdir(prefs.template_folder)


    def execute(self, context):

        prefs = get_addon_preferences()
        
        # check and correct output path

        json_path = prefs.output_manifest_file

        template_folder = prefs.template_folder

        if not os.path.isdir(os.path.dirname(json_path)):
            print(addon_print_prefix + "Incorrect Output Path") #debug
            return {'FINISHED'}

        if not os.path.isdir(template_folder):
            print(addon_print_prefix + "Incorrect Template Folder Path") #debug
            return {'FINISHED'}

        if not json_path.endswith(".json"):
            json_path += ".json"

        # create manifest datas

        manifest_datas = initialize_json_manifest_datas()
        
        for folder in return_direct_subfolders(template_folder):

            # get categories
            category = os.path.basename(folder)
            manifest_datas["categories"].append({"name" : category})

            # get nodetrees
            for subfolder in return_direct_subfolders(folder):
                
                for filepath in return_direct_files(subfolder):

                    if os.path.basename(filepath) == nodetree_infos:

                        nodetree_datas = read_json(filepath)

                        # create json entry for the nodetree
                        nodetree_datas["category"] = category
                        manifest_datas["nodetrees"].append(nodetree_datas)

                        # find better way to check dupe TODO
                        chk_bv = False
                        for b in manifest_datas["blender_versions"]:
                            if b["name"] == nodetree_datas["blender_version"]:
                                chk_bv = True
                                break
                        if not chk_bv:
                            manifest_datas["blender_versions"].append({"name" : nodetree_datas["blender_version"]})

                        chk_av = False
                        for b in manifest_datas["an_versions"]:
                            if b["name"] == nodetree_datas["an_version"]:
                                chk_av = True
                                break
                        if not chk_av:
                            manifest_datas["an_versions"].append({"name" : nodetree_datas["an_version"]})

                        break

        print(addon_print_prefix + "Creating Manifest : " + json_path) #debug

        print(manifest_datas) #debug

        create_json_file(manifest_datas, json_path)

        return {'FINISHED'}