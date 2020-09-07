import bpy
import os


from .global_variables import addon_print_prefix
from .addon_prefs import get_addon_preferences
from .file_functions import create_directory
from .internet_functions import is_connected, download_file


class ANTEMPLATES_OT_import_nodetree(bpy.types.Operator):
    """Edit Nodetree Info File"""
    bl_idname = "antemplates.import_nodetree"
    bl_label = "Import Nodetree"
    bl_options = {'REGISTER', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        winman = bpy.data.window_managers[0]
        properties_coll = winman.an_templates_properties
        nodetree_collection = winman.an_templates_nodetrees
        if properties_coll.nodetrees_index in range(0, len(nodetree_collection)):
            return True


    def execute(self, context):

        winman = context.window_manager
        nodetree_collection = winman.an_templates_nodetrees
        nodetree = nodetree_collection[winman.an_templates_properties.nodetrees_index]

        prefs = get_addon_preferences()

        download_folder = prefs.download_folder

        # create download folder if needed
        if not os.path.isdir(download_folder):
            if not create_directory(download_folder):
                print(addon_print_prefix + "Unable to Create Download Directory") #debug
                return {'FINISHED'}

        nodetree_filepath = os.path.join(download_folder, nodetree.hash)

        # download file if needed
        if not os.path.isfile(nodetree_filepath):

            # check for connection
            if not is_connected():
                print(addon_print_prefix + "No Internet Connection") #debug
                return {'FINISHED'}
            
            # download file
            download_file(nodetree.file_url ,nodetree_filepath)
            print(addon_print_prefix + "Downloading File") #debug
            
            if not os.path.isfile(nodetree_filepath):
                print(addon_print_prefix + "Unable to Download File") #debug
                return {'FINISHED'}

        else:
            print(addon_print_prefix + "Nodetree Already Downloaded") #debug    

        # import nodetree



        print(addon_print_prefix + "Nodetree Successfully Imported") #debug

        return {'FINISHED'}