import bpy
import os


from .json_functions import create_json_file
from .global_variables import addon_print_prefix
from .op_create_manifest import generate_hash


# draw nodetree info properties
def draw_nodetree_info_properties(prop_container, layout, tags_coll):
    layout.prop(prop_container, "name")
    layout.prop(prop_container, "description")
    layout.prop(prop_container, "blender_version")
    layout.prop(prop_container, "an_version")
    layout.prop(prop_container, "image_preview_url")
    layout.prop(prop_container, "video_preview_url")
    layout.prop(prop_container, "file_url")
    layout.prop(prop_container, "readme_url")
    layout.prop(prop_container, "tags")

    col = layout.column(align=True)
    col.label(text="Existing Tags : ")
    limit = 3
    ct = 0
    tag_reformat = ""
    for tag in tags_coll:
        tag_reformat += tag.name
        ct += 1
        if ct == limit:
            col.label(text=tag_reformat)
            tag_reformat = ""
            ct = 0
        else:
            tag_reformat += ", "
    if ct != 0:
        tag_reformat = tag_reformat[:-2]
        col.label(text=tag_reformat)


class ANTEMPLATES_OT_create_nodetree_info(bpy.types.Operator):
    """Create Nodetree Info File"""
    bl_idname = "antemplates.create_nodetree_info"
    bl_label = "Create Nodetree Info"
    bl_options = {'REGISTER', 'INTERNAL'}


    name :              bpy.props.StringProperty(name="Name")
    description :       bpy.props.StringProperty(name="Description")
    blender_version :   bpy.props.StringProperty(name="Blender Version")
    an_version :        bpy.props.StringProperty(name="AN Version")
    tags :              bpy.props.StringProperty(name="Tags")
    image_preview_url : bpy.props.StringProperty(name="Image Preview URL")
    video_preview_url : bpy.props.StringProperty(name="Video Preview URL")
    file_url :          bpy.props.StringProperty(name="File URL")
    readme_url :        bpy.props.StringProperty(name="Readme URL")


    @classmethod
    def poll(cls, context):
        winman = bpy.data.window_managers[0]
        properties_coll = winman.an_templates_properties
        return properties_coll.output_nodetree_info_file != ""


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        draw_nodetree_info_properties(self, self.layout, context.window_manager.an_templates_properties.tags)


    def execute(self, context):

        winman = context.window_manager
        properties_coll = winman.an_templates_properties
        
        # check and correct output path

        json_path = properties_coll.output_nodetree_info_file

        if not os.path.isdir(os.path.dirname(json_path)):
            print(addon_print_prefix + "Incorrect Output Path") #debug
            return {'FINISHED'}

        if not json_path.endswith(".json"):
            json_path += ".json"

        # create dataset
        datas = {}

        datas["name"] =                 self.name
        datas["description"] =          self.description
        datas["blender_version"] =      self.blender_version
        datas["an_version"] =           self.an_version
        datas["tags"] =                 self.tags
        datas["image_preview_url"] =    self.image_preview_url
        datas["video_preview_url"] =    self.video_preview_url
        datas["file_url"] =             self.file_url
        datas["readme_url"] =           self.readme_url
        datas["hash"] =                 generate_hash(10)

        print(addon_print_prefix + "Creating Nodetree Info File : " + json_path) #debug

        print(datas) #debug

        create_json_file(datas, json_path)

        return {'FINISHED'}