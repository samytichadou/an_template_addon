import bpy
import webbrowser

class ANTEMPLATES_OT_open_url(bpy.types.Operator):
    """Open URL in web browser"""
    bl_idname = "antemplates.open_url"
    bl_label = "Open URL"
    bl_options = {'REGISTER', 'INTERNAL'}

    url : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        webbrowser.open(self.url)
        return {'FINISHED'}