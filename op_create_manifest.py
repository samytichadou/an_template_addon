import bpy
import os


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
                        break


        return {'FINISHED'}