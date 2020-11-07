import bpy
import os


addon_name = os.path.basename(os.path.dirname(__file__))

# addon preferences
class ANTEMPLATESAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = addon_name

    custom_library : bpy.props.BoolProperty(
        name = "Custom Library",
        description = "Use Custom Library instead of Animation Nodes Templates Library",
        )

    manifest_url : bpy.props.StringProperty(
        name = "Github Manifest URL",
        default = "",
        )

    download_folder : bpy.props.StringProperty(
        name = "Download Folder",
        default = os.path.join(bpy.utils.user_resource('DATAFILES'), "an_templates"),
        subtype = "DIR_PATH",
        )

    template_folder : bpy.props.StringProperty(
        name="Output Manifest", 
        subtype="DIR_PATH"
        )

    output_manifest_file : bpy.props.StringProperty(
        name="Output Manifest", 
        subtype="FILE_PATH"
        )

    output_newsfeed_file : bpy.props.StringProperty(
        name="Output Newsfeed", 
        subtype="FILE_PATH"
        )


    def draw(self, context):
        
        winman = context.window_manager
        properties_coll = winman.an_templates_properties

        layout = self.layout

        layout.prop(self, "custom_library")
        row = layout.row()
        if not self.custom_library:
            row.enabled=False
        row.prop(self, "manifest_url")
        layout.prop(self, "download_folder")

        bigbox = layout.box()

        bigbox.label(text="Developpers", icon="FILE_SCRIPT")

        box = bigbox.box()
        col = box.column(align=True)
        col.label(text="Manifest")
        col.prop(self, "template_folder", text="Templates")
        col.prop(self, "output_manifest_file", text="Manifest")
        col.operator("antemplates.create_manifest")

        box = bigbox.box()
        col = box.column(align=True)
        col.label(text="Nodetree Infos")
        col.prop(properties_coll, "output_nodetree_info_file", text="")
        col.operator("antemplates.create_nodetree_info")
        col.operator("antemplates.edit_nodetree_info")

        box = bigbox.box()
        col = box.column(align=True)
        col.label(text="Newsfeed")
        col.prop(self, "output_newsfeed_file", text="")
        col.operator("antemplates.create_newsfeed")


# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)