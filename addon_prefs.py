import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

# addon preferences
class ANTEMPLATESAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = addon_name

    manifest_url : bpy.props.StringProperty(
        name = "Github Manifest URL",
        default = "https://raw.githubusercontent.com/samytichadou/an_template_test/master/misc_dev/test.json",
        )

    download_folder : bpy.props.StringProperty(
        name = "Download Folder",
        default = os.path.join(bpy.utils.user_resource('DATAFILES'), "an_templates"),
        subtype = "DIR_PATH",
        )


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "manifest_url")
        layout.prop(self, "download_folder")
        layout.operator("antemplates.create_manifest")


# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)