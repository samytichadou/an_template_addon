import json
import bpy


# read json
def read_json(filepath):
    with open(filepath, "r") as read_file:
        dataset = json.load(read_file)
    return dataset


# set attributes from json
def set_properties_from_dataset(datasetin, datasetout, avoid_list):
    for prop in datasetin:

        chk_avoid = False
        for a in avoid_list:
            if a in prop:
                chk_avoid = True

        if not chk_avoid:

            setattr(datasetout, '%s' % prop, datasetin[prop])


# load json in collection
def loadJsonInCollection(json_file, collection, json_coll_name):
    # remove existing in collection
    collection.clear()

    dataset = read_json(json_file)

    for f in dataset[json_coll_name]:
        
        new = collection.add()
        set_properties_from_dataset(f, new, ())

    return dataset


# set up nodetrees collection from json file
def set_nodetrees_from_json(filepath):
    winman = bpy.data.window_managers[0]
    nodetrees_coll = winman.an_templates_nodetrees
    loadJsonInCollection(filepath, nodetrees_coll, 'nodetrees')


# set up properties collection from json file
def set_properties_from_json(filepath):
    winman = bpy.data.window_managers[0]
    properties_coll = winman.an_templates_properties

    loadJsonInCollection(filepath, properties_coll.blender_versions, 'blender_versions')

    loadJsonInCollection(filepath, properties_coll.an_versions, 'an_versions')

    loadJsonInCollection(filepath, properties_coll.categories, 'categories')