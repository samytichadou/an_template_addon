import bpy
import webbrowser


from .global_variables import addon_print_prefix


class ANTEMPLATES_OT_open_url(bpy.types.Operator):
    """Open URL in web browser"""
    bl_idname = "antemplates.open_url"
    bl_label = "Open URL"
    bl_options = {'REGISTER', 'INTERNAL'}

    url : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        properties_coll = winman.an_templates_properties
        nodetree_collection = winman.an_templates_nodetrees
        if properties_coll.nodetrees_index in range(0, len(nodetree_collection)):
            return True

    def execute(self, context):
        if self.url == "":
            print(addon_print_prefix + "No URL to Open")
        else:
            webbrowser.open(self.url)
            print(addon_print_prefix + "Opening URL in Web Browser : %s" % self.url)
        return {'FINISHED'}