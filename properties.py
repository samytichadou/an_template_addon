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

class ANTemplatesProperties(bpy.types.PropertyGroup) :
    '''name : StringProperty() '''
    blender_versions : bpy.props.CollectionProperty(type = ANTemplatesBlenderVersions, name="Blender Versions")
    an_versions : bpy.props.CollectionProperty(type = ANTemplatesANVersions, name="Animation Nodes Verions")
    categories : bpy.props.CollectionProperty(type = ANTemplatesCategories, name="Categories")
    nodetrees_index : bpy.props.IntProperty(name="Nodetrees Index")
    manifest_hash : bpy.props.StringProperty(name="Manifest Hash")