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

        layout.template_list("ANTEMPLATES_UL_panel_ui_list", "", winman, "an_templates_nodetrees", winman.an_templates_properties, "nodetrees_index", rows = 3)
        
        layout.operator("antemplates.import_nodetree")

        # import nodetree properties
        # make it responsive TODO
        col = layout.column(align=True)
        col.prop(properties_coll, "import_original_scene")
        col.prop(properties_coll, "keep_original_objects")

        col2 = layout.column(align=True)
        if not properties_coll.import_original_scene and properties_coll.keep_original_objects:
            col2.enabled=True
        else:
            col2.enabled=False
        col2.prop(properties_coll, "original_objects_collection", text="")
        row = col2.row()
        if properties_coll.original_objects_collection != "SPECIFIC":
            row.enabled=False
        row.prop(properties_coll, "original_object_specific_collection", text="")

        # nodetree properties
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
