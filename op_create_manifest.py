import bpy
import os
import string
import random

from .json_functions import read_json, create_json_file


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
    bl_options = {'REGISTER'}#, 'INTERNAL'}

    github_url : bpy.props.StringProperty(name="Github URL")

    template_folder : bpy.props.StringProperty(name="Template Folder")

    output_path : bpy.props.StringProperty(name="Output Path")

    @classmethod
    def poll(cls, context):
        return True


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "github_url")
        layout.prop(self, "template_folder")
        layout.prop(self, "output_path")


    def execute(self, context):
        
        # check and correct output path

        json_path = self.output_path

        if not os.path.isdir(os.path.dirname(json_path)):
            print("Incorrect Output Path") #debug
            return {'FINISHED'}

        if not json_path.endswith(".json"):
            json_path += ".json"
            print(json_path) #debug

        manifest_datas = initialize_json_manifest_datas()
        
        for folder in return_direct_subfolders(self.template_folder):

            # get categories
            category = os.path.basename(folder)
            manifest_datas["categories"].append({"name" : category})

            # get nodetrees
            for subfolder in return_direct_subfolders(folder):
                
                for filepath in return_direct_files(subfolder):

                    if os.path.basename(filepath) == "nodetree_infos.json":

                        nodetree_datas = read_json(filepath)

                        # create json entry for the nodetree
                        nodetree_datas["category"] = category
                        manifest_datas["nodetrees"].append(nodetree_datas)

                        if nodetree_datas["blender_version"] not in manifest_datas["blender_versions"]:
                            manifest_datas["blender_versions"].append({"name" : nodetree_datas["blender_version"]})

                        if nodetree_datas["an_version"] not in manifest_datas["an_versions"]:
                            manifest_datas["an_versions"].append({"name" : nodetree_datas["an_version"]})

                        break

        print("Creating manifest") #debug

        print(manifest_datas) #debug

        create_json_file(manifest_datas, json_path)

        return {'FINISHED'}