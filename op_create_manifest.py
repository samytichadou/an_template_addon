import bpy
import os


class ANTEMPLATES_OT_create_manifest(bpy.types.Operator):
    """Create Manifest from Github URL and Template Folder"""
    bl_idname = "antemplates.create_manifest"
    bl_label = "Create Manifest"
    bl_options = {'REGISTER', 'INTERNAL'}

    github_url : bpy.props.StringProperty(name="Github URL")

    template_folder : bpy.props.StringProperty(name="Template Folder")

    @classmethod
    def poll(cls, context):
        return True


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "github_url")
        layout.prop(self, "template_folder")


    def execute(self, context):

    

        return {'FINISHED'}