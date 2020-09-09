import bpy
import os


from .global_variables import addon_print_prefix
from .addon_prefs import get_addon_preferences
from .file_functions import create_directory
from .internet_functions import is_connected, download_file


# clear lib user
def clearDataUsers(lib):
    lib.use_fake_user = False

    try:
        for datas in lib.users_id:
            datas.use_fake_user = False
            datas.user_clear()

    except AttributeError:
        print("F")
        pass

    lib.user_clear()


# link nodetree
def link_nodetree(filepath, name, properties_coll, context):
    active_scene = context.scene
    original_scene = properties_coll.import_original_scene
    original_objects = properties_coll.keep_original_objects
    collection_behavior = properties_coll.original_objects_collection

    imported = []
    lib = bpy.data.libraries.load(filepath, link=False, relative=True)


    # get old scenes and collections

    old_scenes = []
    for scn in bpy.data.scenes:
        old_scenes.append(scn)

    old_collections = []
    for coll in bpy.data.collections:
        old_collections.append(coll)


     # import nodetree

    with lib as (data_from, data_to):
        data_to.node_groups = data_from.node_groups

    for new_node in data_to.node_groups:

        if new_node.bl_idname == "an_AnimationNodeTree":
            if new_node.name == name:
                imported.append(new_node)
            elif name + ".00" in new_node.name:
                bpy.data.node_groups.remove(bpy.data.node_groups[new_node.name])
                print(addon_print_prefix + "Nodetree already exists, remove it") #debug
            else:
                bpy.data.node_groups.remove(bpy.data.node_groups[new_node.name])

        else:
            bpy.data.node_groups.remove(bpy.data.node_groups[new_node.name])


    # return if not imported

    if len(imported) == 0:

        # remove new scenes if needed
        for scn in bpy.data.scenes:
            if scn in old_scenes:
                continue
            else:
                for object in scn.objects:
                    bpy.data.objects.remove(object, do_unlink=True)
                bpy.data.scenes.remove(scn, do_unlink=True)

        return False


    # deal with objects 

    if not original_objects:
        for scn in bpy.data.scenes:
            if scn in old_scenes:
                continue
            else:
                for object in scn.objects:
                    bpy.data.objects.remove(object, do_unlink=True)

    elif original_objects and not original_scene:
        
        # target collection
        if collection_behavior == "SPECIFIC":
            try:
                coll = active_scene.collection.children[properties_coll.original_object_specific_collection]
            except KeyError:
                coll = bpy.data.collections.new(properties_coll.original_object_specific_collection)
                old_collections.append(coll)
                active_scene.collection.children.link(coll)
        elif collection_behavior == "SCENE":
            coll = active_scene.collection
        else:
            coll = context.collection

        # an collection
        try:
            an_coll = bpy.data.collections["Animation Nodes Object Container"]
        except KeyError:
            an_coll = bpy.data.collections.new("Animation Nodes Object Container")
        
        try:
            active_scene.collection.children.link(an_coll)
        except RuntimeError:
            pass

        # get objects
        chk_instances = False
        for scn in bpy.data.scenes:
            if scn in old_scenes:
                continue
            else:
                for object in scn.objects:
                    if "instance_" not in object.name:
                        coll.objects.link(object)
                    else:
                        chk_instances = True

        if chk_instances:
            old_collections.append(an_coll)


    # deal with collections

    #remove new collections if needed
    if original_objects and original_scene:
        pass
    else:
        for coll in bpy.data.collections:
            if coll in old_collections:
                continue
            else:
                bpy.data.collections.remove(coll, do_unlink=True)
    

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
                bpy.data.scenes.remove(scn, do_unlink=True)


    # deal with library

    blend_name = os.path.basename(filepath)

    if bpy.data.libraries[blend_name]:

        clearDataUsers(bpy.data.libraries[blend_name])

        #bpy.data.orphans_purge()


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
            print(addon_print_prefix + "Downloading File") #debug
            download_file(nodetree.file_url ,nodetree_filepath)
            
            if not os.path.isfile(nodetree_filepath):
                print(addon_print_prefix + "Unable to Download File") #debug
                return {'FINISHED'}

        else:
            print(addon_print_prefix + "Nodetree Already Downloaded") #debug    

        print(addon_print_prefix + "Importing : " + nodetree.name) #debug

        # import nodetree
        if link_nodetree(nodetree_filepath, nodetree.name, properties_coll, context):

            print(addon_print_prefix + "Nodetree Successfully Imported") #debug

        else:

            print(addon_print_prefix + "Unable to Import Nodetree") #debug

        return {'FINISHED'}