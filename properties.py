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
    downloaded : bpy.props.BoolProperty(name="Available Offline")


class ANTemplatesBlenderVersions(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''


class ANTemplatesANVersions(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''


class ANTemplatesCategories(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''


class ANTemplatesTags(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''


class ANTemplatesNews(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    url : bpy.props.StringProperty(name="News URL")
    nodetree_name : bpy.props.StringProperty(name="Nodetree Name")


def get_categories_callback(scene, context):

    items = []

    items.append(("ALL", "All", ""))

    for i in context.window_manager.an_templates_properties.categories:
        items.append((i.name, i.name, ""))

    return items


def get_categories_submission_callback(scene, context):

    items = []

    items.append(("CHOOSE_CATEGORY", "Choose Category", ""))
    items.append(("NEW_CATEGORY", "New Category", ""))

    for i in context.window_manager.an_templates_properties.categories:
        items.append((i.name, i.name, ""))

    return items


def get_an_nodetree_callback(scene, context):

    items = []

    items.append(("CHOOSE_NODETREE", "Choose NodeTree", ""))

    for n in bpy.data.node_groups:
        if n.bl_idname == "an_AnimationNodeTree":
            items.append((n.name, n.name, ""))

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
    
    nodetree_search : bpy.props.StringProperty(name="Search", description = "Search for Nodetree and Tags if activated, use a + between Tags", options={'TEXTEDIT_UPDATE','SKIP_SAVE'})
    nodetree_tag_search : bpy.props.BoolProperty(name="Tag Search Toggle", default = True)

    submission_nodetree : bpy.props.EnumProperty(name="Nodetree", description="Submitted NodeTree", items = get_an_nodetree_callback)
    submission_readme : bpy.props.PointerProperty(name="Readme", description="Extensive Description of the Nodetree and How to use it in a Text Block", type=bpy.types.Text)
    submission_tags : bpy.props.StringProperty(name="Tags, Comma Separated")
    submission_category : bpy.props.EnumProperty(name="Category", items = get_categories_submission_callback)
    submission_small_description : bpy.props.StringProperty(name="Small Description")
    submission_image_preview_url : bpy.props.StringProperty(name="Image Preview URL", description="Add Custom Image Preview, if Empty, a blender screenshot will be used", subtype="FILE_PATH")
    submission_video_preview_url : bpy.props.StringProperty(name="Video Preview URL")
    submission_author_mail : bpy.props.StringProperty(name="Your Mail")
    submission_author_name : bpy.props.StringProperty(name="Your Name")
    submission_side_notes : bpy.props.StringProperty(name="Side Notes")

    k_v : bpy.props.StringProperty()

    update_needed : bpy.props.BoolProperty()
    update_message : bpy.props.StringProperty()
    update_download_url : bpy.props.StringProperty()

    #newsfeed
    newsfeed_hash : bpy.props.StringProperty(name="Newsfeed Hash")
    news : bpy.props.CollectionProperty(type = ANTemplatesNews, name="News")
    temp_news : bpy.props.CollectionProperty(type = ANTemplatesNews, name="Temp News")
    active_news : bpy.props.IntProperty()