import bpy
import os


from .global_variables import addon_print_prefix
from .addon_prefs import get_addon_preferences
from .file_functions import create_directory
from .internet_functions import is_connected, download_file


# clear lib user
def clearDataUsers(lib):
    lib.use_fake_user = False
    while lib.users != 0:
        lib.user_clear()
    try:
        for datas in lib.users_id:
            datas.use_fake_user = False
            datas.user_clear()
    except AttributeError:
        pass


# link nodetree
def link_nodetree(filepath, name):

    imported = []
    lib = bpy.data.libraries.load(filepath, link=False, relative=True)
    #blend_name = os.path.basename(filepath)

    # import

    with lib as (data_from, data_to):
        data_to.node_groups = data_from.node_groups

    for new_node in data_to.node_groups:

        if new_node.bl_idname != "an_AnimationNodeTree" or new_node.name != name:
            bpy.data.node_groups.remove(bpy.data.node_groups[new_node.name])
        else:
           imported.append(new_node)

    # remove lib
    #clearDataUsers(bpy.data.libraries[blend_name])
    #bpy.data.orphans_purge()


    if len(imported) == 0:
        return False
    else:
        return True


# link nodetree
def old_link_nodetree(filepath, name):
    path = os.path.join(filepath, "NodeTree")
    bpy.ops.wm.append(filename=name, directory=path)


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

        print(addon_print_prefix + "Importing : " + nodetree.name) #debug

        # import nodetree
        if link_nodetree(nodetree_filepath, nodetree.name):

            print(addon_print_prefix + "Nodetree Successfully Imported") #debug

        else:

            print(addon_print_prefix + "Unable to Import Nodetree") #debug

        return {'FINISHED'}