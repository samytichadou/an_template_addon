import bpy
import os

from . import addon_updater_ops

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

    # auto-updater
    auto_check_update : bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False,
		)
    updater_intrval_months : bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0
		)
    updater_intrval_days : bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31
		)
    updater_intrval_hours : bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23
		)
    updater_intrval_minutes : bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59
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

        bigbox.label(text="Developpers", icon="SCRIPT")

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

        # auto-updater
        addon_updater_ops.update_settings_ui(self,context)


# get addon preferences
def get_addon_preferences():
    addon = bpy.context.preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)