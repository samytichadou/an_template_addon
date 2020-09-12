import bpy


class ANTemplatesNodetrees(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    description : bpy.props.StringProperty(name="Description")
    blender_version : bpy.props.StringProperty(name="Blender Version")
    an_version : bpy.props.StringProperty(name="Animation Nodes Version")
    category : bpy.props.StringProperty(name="Category")
    tags : bpy.props.StringProperty(name="Tags")
    hash : bpy.props.StringProperty(name="Nodetree Hash")
    image_preview_url : bpy.props.StringProperty(name="Image Preview")
    video_preview_url : bpy.props.StringProperty(name="Video Preview")
    file_url : bpy.props.StringProperty(name="File URL")
    readme_url : bpy.props.StringProperty(name="Readme URL")


class ANTemplatesBlenderVersions(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''


class ANTemplatesANVersions(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''


class ANTemplatesCategories(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''


class ANTemplatesTags(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''


def get_categories_callback(scene, context):

    items = []

    items.append(("ALL", "All", ""))

    for i in context.window_manager.an_templates_properties.categories:
        items.append((i.name, i.name, ""))

    return items


class ANTemplatesProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    blender_versions : bpy.props.CollectionProperty(type = ANTemplatesBlenderVersions, name="Blender Versions")
    an_versions : bpy.props.CollectionProperty(type = ANTemplatesANVersions, name="Animation Nodes Verions")
    categories : bpy.props.CollectionProperty(type = ANTemplatesCategories, name="Categories")
    tags : bpy.props.CollectionProperty(type = ANTemplatesTags, name="Tags")
    nodetrees_index : bpy.props.IntProperty(name="Nodetrees Index")
    manifest_hash : bpy.props.StringProperty(name="Manifest Hash")

    import_original_scene : bpy.props.BoolProperty(name="Import Original Scene")
    keep_original_objects : bpy.props.BoolProperty(name="Keep Original Objects")
    original_object_specific_collection : bpy.props.StringProperty(name="Specific Collection", default = "Collection")
    original_objects_collection_items = [
        ('SPECIFIC', 'Specific', ""),
        ('ACTIVE', 'Active', ""),
        ('SCENE', 'Scene', ""),
        ]
    original_objects_collection : bpy.props.EnumProperty(name="Original Objects Collection", items = original_objects_collection_items, default='SCENE')

    output_nodetree_info_file : bpy.props.StringProperty(name="Output Nodetree Info", subtype="FILE_PATH")

    show_import_options : bpy.props.BoolProperty(name="Show Import Options")
    show_nodetree_infos : bpy.props.BoolProperty(name="Show Nodetree Infos")

    nodetree_categories_enum : bpy.props.EnumProperty(name="Categories", items = get_categories_callback)
    
    nodetree_search : bpy.props.StringProperty(name = "Search", description = "Search for Nodetree and Tags if activated, use a + between Tags", options={'TEXTEDIT_UPDATE','SKIP_SAVE'})
    nodetree_tag_search : bpy.props.BoolProperty(name = "Tag Search Toggle", default = True)