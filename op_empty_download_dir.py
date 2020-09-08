import bpy
import os


from .addon_prefs import get_addon_preferences
from .file_functions import empty_directory
from .global_variables import addon_print_prefix


class ANTEMPLATES_OT_clear_downloads(bpy.types.Operator):
    """Clear existing templates"""
    bl_idname = "antemplates.clear_downloads"
    bl_label = "Clear Downloads"
    bl_options = {'REGISTER', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.label(text="You are about to delete downloaded templates", icon="QUESTION")
        layout.label(text="Are you sure ?")


    def execute(self, context):

        prefs = get_addon_preferences()
        download_folder = prefs.download_folder

        if os.path.isdir(download_folder):
            empty_directory(download_folder)

        else:
            print(addon_print_prefix + "Download directory does not exist : %s" % download_folder) #debug

        return {'FINISHED'}