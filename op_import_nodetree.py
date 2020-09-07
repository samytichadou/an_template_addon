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
def link_nodetree(filepath, name, original_scene, active_scene):

    old_scenes = []
    for scn in bpy.data.scenes:
        old_scenes.append(scn)

    imported = []
    lib = bpy.data.libraries.load(filepath, link=False, relative=True)

    # import nodetree

    with lib as (data_from, data_to):
        data_to.node_groups = data_from.node_groups

    for new_node in data_to.node_groups:

        if new_node.bl_idname != "an_AnimationNodeTree" or new_node.name != name:
            bpy.data.node_groups.remove(bpy.data.node_groups[new_node.name])
        else:
           imported.append(new_node)

    # deal with scenes 

    if not original_scene:

        # set nodetree active scene
        for nodetree in imported:
            nodetree.globalScene = active_scene

        # remove new scenes if needed
        for scn in bpy.data.scenes:
            if scn in old_scenes:
                continue
            else:
                # remove or move objects from scene TODO
                bpy.data.scenes.remove(scn, do_unlink=True)


    # return if imported

    if len(imported) == 0:
        # remove scenes if imported TODO
        return False
    else:
        # if nodetree already imported, extra scenes, remove them TODO
        return True



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
        properties_coll = winman.an_templates_properties
        nodetree = nodetree_collection[properties_coll.nodetrees_index]
        original_scene = properties_coll.import_original_scene

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
        if link_nodetree(nodetree_filepath, nodetree.name, original_scene, context.scene):

            print(addon_print_prefix + "Nodetree Successfully Imported") #debug

        else:

            print(addon_print_prefix + "Unable to Import Nodetree") #debug

        return {'FINISHED'}