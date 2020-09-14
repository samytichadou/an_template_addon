import bpy
import os


from .addon_prefs import get_addon_preferences
from .file_functions import create_directory
from .internet_functions import is_connected, download_file
from .print_functions import print_and_report


# clear lib user
def clearDataUsers(lib):
    lib.use_fake_user = False

    try:
        for datas in lib.users_id:
            datas.use_fake_user = False
            datas.user_clear()

    except AttributeError:
        pass

    lib.user_clear()


# create an collection for scene
def return_an_collection(target_scene):

    try:
        an_coll = bpy.data.collections["Animation Nodes Object Container"]
    except KeyError:
        an_coll = bpy.data.collections.new("Animation Nodes Object Container")

    try:
        target_scene.collection.children.link(an_coll)
    except RuntimeError:
        pass

    return an_coll


def link_nodetree(filepath, name, self, context):
    active_scene = context.scene
    properties_coll = context.window_manager.an_templates_properties
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


    # get target coll and an target coll if needed 
    if not original_scene and original_objects:
        # target coll
        if collection_behavior == "SPECIFIC":
            try:
                target_coll = active_scene.collection.children[properties_coll.original_object_specific_collection]
            except KeyError:
                target_coll = bpy.data.collections.new(properties_coll.original_object_specific_collection)
                old_collections.append(target_coll)
                active_scene.collection.children.link(target_coll)
        elif collection_behavior == "SCENE":
            target_coll = active_scene.collection
        else:
            target_coll = context.collection


    # import nodetree

    with lib as (data_from, data_to):
        data_to.node_groups = data_from.node_groups

    for new_node in data_to.node_groups:

        if new_node.bl_idname == "an_AnimationNodeTree":
            if new_node.name == name:
                imported.append(new_node)
            elif name + ".00" in new_node.name:
                bpy.data.node_groups.remove(bpy.data.node_groups[new_node.name])
                print_and_report(None, "Nodetree already exists, remove it", "WARNING") #debug
            else:
                bpy.data.node_groups.remove(bpy.data.node_groups[new_node.name])

        else:
            bpy.data.node_groups.remove(bpy.data.node_groups[new_node.name])


    # return if not imported

    if len(imported) == 0:

        # remove scenes and objects
        for scn in bpy.data.scenes:
            if scn not in old_scenes:
                for object in scn.objects:
                    bpy.data.objects.remove(object, do_unlink=True)
                bpy.data.scenes.remove(scn, do_unlink=True)

        # remove collections
        for coll in bpy.data.collections:
            if coll not in old_collections:
                bpy.data.collections.remove(coll, do_unlink=True)

        return False


    # not scn / not obj
    if not original_scene and not original_objects:

        # remove scenes and objects
        for scn in bpy.data.scenes:
            if scn not in old_scenes:
                for object in scn.objects:
                    bpy.data.objects.remove(object, do_unlink=True)
                bpy.data.scenes.remove(scn, do_unlink=True)

        # remove collections
        for coll in bpy.data.collections:
            if coll not in old_collections:
                bpy.data.collections.remove(coll, do_unlink=True)


    # scn / not obj
    elif original_scene and not original_objects:

        # remove objects
        for scn in bpy.data.scenes:
            if scn not in old_scenes:
                for object in scn.objects:
                    bpy.data.objects.remove(object, do_unlink=True)

        # remove collections
        for coll in bpy.data.collections:
            if coll not in old_collections:
                bpy.data.collections.remove(coll, do_unlink=True)


    # not scn / obj
    elif not original_scene and original_objects:

        # link collections
        for coll in bpy.data.collections:
            if coll not in old_collections:

                if coll.name == "Animation Nodes Object Container":
                    active_scene.collection.children.link(coll)

                elif "Animation Nodes Object Container.00" in coll.name:
                    an_coll = return_an_collection(active_scene)
                    for obj in coll.objects:
                        an_coll.objects.link(obj)
                    bpy.data.collections.remove(coll, do_unlink=True)

                else:
                    for obj in coll.objects:
                        target_coll.objects.link(obj)
                    bpy.data.collections.remove(coll, do_unlink=True)

        # remove scenes and get obj from its root collection
        for scn in bpy.data.scenes:
            if scn not in old_scenes:
                for obj in scn.collection.objects:
                    target_coll.objects.link(obj)
                bpy.data.scenes.remove(scn, do_unlink=True)

    
    # scn / obj
    elif original_scene and original_objects:
        
        # target scene
        for nodetree in imported:
            target_scn = nodetree.globalScene
            break

        # link an collection if needed
        for coll in bpy.data.collections:
            if coll not in old_collections:

                if "Animation Nodes Object Container.00" in coll.name:
                    an_coll = return_an_collection(target_scn)
                    for obj in coll.objects:
                        an_coll.objects.link(obj)
                    bpy.data.collections.remove(coll, do_unlink=True)


    # set nodetree active scene if needed
    if not original_scene:
        for nodetree in imported:
            nodetree.globalScene = active_scene

    return True


class ANTEMPLATES_OT_import_nodetree(bpy.types.Operator):
    """Edit Nodetree Info File"""
    bl_idname = "antemplates.import_nodetree"
    bl_label = "Import Nodetree"
    bl_options = {'REGISTER', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        winman = context.window_manager
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
                print_and_report(self, "Unable to Create Download Directory", "WARNING") #debug
                return {'FINISHED'}

        nodetree_filepath = os.path.join(download_folder, nodetree.hash)

        # download file if needed
        if not os.path.isfile(nodetree_filepath):

            # check for connection
            if not is_connected():
                print_and_report(self, "No Internet Connection", "WARNING") #debug
                return {'FINISHED'}
            
            # download file
            print_and_report(None, "Downloading File", "INFO") #debug
            download_file(nodetree.file_url ,nodetree_filepath)
            
            if not os.path.isfile(nodetree_filepath):
                print_and_report(self, "Unable to Download File", "WARNING") #debug
                return {'FINISHED'}

            else:
                nodetree.downloaded = True

        else:
            print_and_report(None, "Nodetree Already Downloaded", "INFO") #debug

        print_and_report(None, "Importing : " + nodetree.name, "INFO") #debug

        # import nodetree
        if link_nodetree(nodetree_filepath, nodetree.name, self, context):

            print_and_report(self, "Nodetree Successfully Imported", "INFO") #debug

        else:

            print_and_report(self, "Unable to Import Nodetree", "WARNING") #debug

        return {'FINISHED'}