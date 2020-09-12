import bpy
import os


from .json_functions import create_json_file, read_json
from .op_create_manifest import generate_hash
from .op_create_nodetree_info import draw_nodetree_info_properties
from .print_functions import print_and_report


class ANTEMPLATES_OT_edit_nodetree_info(bpy.types.Operator):
    """Edit Nodetree Info File"""
    bl_idname = "antemplates.edit_nodetree_info"
    bl_label = "Edit Nodetree Info"
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
    hash :              bpy.props.StringProperty(name="Hash")


    @classmethod
    def poll(cls, context):
        winman = bpy.data.window_managers[0]
        properties_coll = winman.an_templates_properties
        return os.path.isfile(properties_coll.output_nodetree_info_file)


    def invoke(self, context, event):

        winman = context.window_manager
        json_path = winman.an_templates_properties.output_nodetree_info_file
        datas = read_json(json_path)
        
        # fill properties from json

        self.name =                 datas["name"]
        self.description =          datas["description"]
        self.blender_version =      datas["blender_version"]
        self.an_version =           datas["an_version"]
        self.tags =                 datas["tags"]
        self.image_preview_url =    datas["image_preview_url"]
        self.video_preview_url =    datas["video_preview_url"]
        self.file_url =             datas["file_url"]
        self.readme_url =           datas["readme_url"]
        self.hash =                 datas["hash"]
            
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout

        draw_nodetree_info_properties(self, layout, context.window_manager.an_templates_properties.tags)

        layout.label(text="Hash : " + self.hash)


    def execute(self, context):

        winman = context.window_manager
        json_path = winman.an_templates_properties.output_nodetree_info_file

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

        print_and_report(None, "Creating Nodetree Info File : " + json_path, "INFO") #debug

        print(datas) #debug

        create_json_file(datas, json_path)

        print_and_report(self, "Nodetree Info File Successfully Created", "INFO") #debug

        return {'FINISHED'}