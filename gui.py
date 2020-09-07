import bpy


class ANTEMPLATES_PT_panel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_panel"
    bl_label = "Templates"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Templates"

    @classmethod
    def poll(cls, context):
        if context.area.type == "NODE_EDITOR":
            if context.area.ui_type == "an_AnimationNodeTree":
                return True

    def draw(self, context):

        winman = context.window_manager
        properties_coll = winman.an_templates_properties

        layout = self.layout

        layout.operator('antemplates.clear_downloads', icon="TRASH")

        box = layout.box()
        col = box.column(align=True)
        col.label(text="Manifest")
        col.prop(properties_coll, "template_folder", text="Templates")
        col.prop(properties_coll, "output_manifest_file", text="Manifest")
        col.operator("antemplates.create_manifest")

        box = layout.box()
        col = box.column(align=True)
        col.label(text="Nodetree Infos")
        col.prop(properties_coll, "output_nodetree_info_file", text="")
        col.operator("antemplates.create_nodetree_info")
        col.operator("antemplates.edit_nodetree_info")

        layout.template_list("ANTEMPLATES_UL_panel_ui_list", "", winman, "an_templates_nodetrees", winman.an_templates_properties, "nodetrees_index", rows = 3)


        idx = winman.an_templates_properties.nodetrees_index

        if idx in range(0, len(winman.an_templates_nodetrees)):
            active_nodetree = winman.an_templates_nodetrees[winman.an_templates_properties.nodetrees_index]
            
            col = layout.column(align=True)

            col.label(text=active_nodetree.description, icon="INFO")
            col.label(text=active_nodetree.blender_version, icon="BLENDER")
            col.label(text=active_nodetree.an_version, icon="ONIONSKIN_ON")
            col.label(text=active_nodetree.category, icon="FILE_FOLDER")
            col.label(text=active_nodetree.tags, icon="VIEWZOOM")
            col.label(text=active_nodetree.hash, icon="RNA")
            col.label(text=active_nodetree.file_url, icon="URL")
