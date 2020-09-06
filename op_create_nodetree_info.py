import bpy
import os


from .json_functions import create_json_file


class ANTEMPLATES_OT_create_nodetree_info(bpy.types.Operator):
    """Create Nodetree Info File"""
    bl_idname = "antemplates.create_nodetree_info"
    bl_label = "Create Nodetree Info"
    bl_options = {'REGISTER'}#, 'INTERNAL'}

    output_path :       bpy.props.StringProperty(name="Output Path")

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
        return True


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout

        layout.prop(self, "output_path")

        layout.prop(self, "name")
        layout.prop(self, "description")
        layout.prop(self, "blender_version")
        layout.prop(self, "an_version")
        layout.prop(self, "tags")
        layout.prop(self, "image_preview_url")
        layout.prop(self, "video_preview_url")
        layout.prop(self, "file_url")
        layout.prop(self, "readme_url")


    def execute(self, context):
        
        # check and correct output path

        json_path = self.output_path

        if not os.path.isdir(os.path.dirname(json_path)):
            print("Incorrect Output Path") #debug
            return {'FINISHED'}

        if not json_path.endswith(".json"):
            json_path += ".json"
            print(json_path) #debug

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

        print("Creating nodetree info file") #debug

        print(datas) #debug

        create_json_file(datas, json_path)

        return {'FINISHED'}