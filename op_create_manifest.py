import bpy
import os
import string
import random


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


# get nodetrees infos from md file
def get_infos_from_md(file):

    infos = []

    # Using readlines() 
    file1 = open(file, 'r') 
    Lines = file1.readlines() 
    
    # Strips the newline character 
    for line in Lines: 

        if line.startswith("__"):
            
            prop_id = (line.split("__")[1]).split(" :")[0]
            prop_value = (line.split(" : ")[1]).split("\n")[0]
            
            infos.append([prop_id, prop_value])

    return infos


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

    @classmethod
    def poll(cls, context):
        return True


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "github_url")
        layout.prop(self, "template_folder")


    def execute(self, context):

        categories = []

        manifest_datas = initialize_json_manifest_datas()
        
        for folder in return_direct_subfolders(self.template_folder):

            # get categories
            categories.append(os.path.basename(folder))
            print(folder)

            # get nodetrees
            for subfolder in return_direct_subfolders(folder):
                
                for filepath in return_direct_files(subfolder):

                    if os.path.basename(filepath) == "readme.md":

                        readme_file = filepath

                        # create json entry for the nodetree

                        nodetree_infos = get_infos_from_md(readme_file)

                        for data in nodetree_infos:
                            print(data)
                            

                        break


        return {'FINISHED'}