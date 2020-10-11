import bpy
import os
import string
import random


from .json_functions import read_json, create_json_file
from .global_variables import nodetree_infos, global_k_filepath
from .addon_prefs import get_addon_preferences
from .print_functions import print_and_report


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
    datas = read_json(global_k_filepath)
    return datas["k"], datas["w"], datas["v"]


# initialize json manifest datas
def initialize_json_manifest_datas() :

    datas = {}

    datas["nodetrees"] = []
    datas["blender_versions"] = []
    datas["an_versions"] = []
    datas["categories"] = []
    datas["tags"] = []
    datas["manifest_hash"] = generate_hash(10)
    datas["k_v"] = get_global_k()[2]

    return datas


# get separated tags
def get_separated_tags(tag_line):
    tags = []
    if tag_line != "":
        for t in tag_line.split(","):
            tags.append(t.strip())
    return tags


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

        print(manifest_datas) #debug

        create_json_file(manifest_datas, json_path)

        print_and_report(self, "Manifest Successfully Created", "INFO") #debug

        return {'FINISHED'}