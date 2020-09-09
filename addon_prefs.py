import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

# addon preferences
class ANTEMPLATESAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = addon_name

    manifest_url : bpy.props.StringProperty(
        name = "Github Manifest URL",
        default = "https://raw.githubusercontent.com/samytichadou/animation_nodes_examples/master/library/manifest.json",
        )

    download_folder : bpy.props.StringProperty(
        name = "Download Folder",
        default = os.path.join(bpy.utils.user_resource('DATAFILES'), "an_templates"),
        subtype = "DIR_PATH",
        )


    def draw(self, context):
        winman = context.window_manager
        properties_coll = winman.an_templates_properties

        layout = self.layout
        layout.prop(self, "manifest_url")
        layout.prop(self, "download_folder")

        bigbox = layout.box()

        bigbox.label(text="Developpers", icon="SCRIPT")

        box = bigbox.box()
        col = box.column(align=True)
        col.label(text="Manifest")
        col.prop(properties_coll, "template_folder", text="Templates")
        col.prop(properties_coll, "output_manifest_file", text="Manifest")
        col.operator("antemplates.create_manifest")

        box = bigbox.box()
        col = box.column(align=True)
        col.label(text="Nodetree Infos")
        col.prop(properties_coll, "output_nodetree_info_file", text="")
        col.operator("antemplates.create_nodetree_info")
        col.operator("antemplates.edit_nodetree_info")


# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)