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


# Image Preview
class ANTEMPLATES_OT_open_url_image(bpy.types.Operator):
    """Open Image Preview in Web Browser"""
    bl_idname = "antemplates.open_url_image"
    bl_label = "Open Image Preview"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        properties_coll = winman.an_templates_properties
        nodetree_collection = winman.an_templates_nodetrees
        if properties_coll.nodetrees_index in range(0, len(nodetree_collection)):
            if nodetree_collection[properties_coll.nodetrees_index].image_preview_url:
                return True

    def execute(self, context):
        winman = context.window_manager
        properties_coll = winman.an_templates_properties
        nodetree_collection = winman.an_templates_nodetrees
        url = nodetree_collection[properties_coll.nodetrees_index].image_preview_url

        webbrowser.open(url)
        print(addon_print_prefix + "Opening URL in Web Browser : %s" % url)
        return {'FINISHED'}


# Video Preview
class ANTEMPLATES_OT_open_url_video(bpy.types.Operator):
    """Open Video Preview in Web Browser"""
    bl_idname = "antemplates.open_url_video"
    bl_label = "Open Video Preview"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        properties_coll = winman.an_templates_properties
        nodetree_collection = winman.an_templates_nodetrees
        if properties_coll.nodetrees_index in range(0, len(nodetree_collection)):
            if nodetree_collection[properties_coll.nodetrees_index].video_preview_url:
                return True

    def execute(self, context):
        winman = context.window_manager
        properties_coll = winman.an_templates_properties
        nodetree_collection = winman.an_templates_nodetrees
        url = nodetree_collection[properties_coll.nodetrees_index].video_preview_url

        webbrowser.open(url)
        print(addon_print_prefix + "Opening URL in Web Browser : %s" % url)
        return {'FINISHED'}


# Readme
class ANTEMPLATES_OT_open_url_readme(bpy.types.Operator):
    """Open Readme in Web Browser"""
    bl_idname = "antemplates.open_url_readme"
    bl_label = "Open Readme"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        winman = context.window_manager
        properties_coll = winman.an_templates_properties
        nodetree_collection = winman.an_templates_nodetrees
        if properties_coll.nodetrees_index in range(0, len(nodetree_collection)):
            if nodetree_collection[properties_coll.nodetrees_index].readme_url:
                return True

    def execute(self, context):
        winman = context.window_manager
        properties_coll = winman.an_templates_properties
        nodetree_collection = winman.an_templates_nodetrees
        url = nodetree_collection[properties_coll.nodetrees_index].readme_url

        webbrowser.open(url)
        print(addon_print_prefix + "Opening URL in Web Browser : %s" % url)
        return {'FINISHED'}