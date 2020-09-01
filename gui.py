import bpy


class ANTEMPLATES_PT_panel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_auto_execution_panel"
    bl_label = "Templates"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Templates"

    @classmethod
    def poll(cls, context):
        # tree = cls.getTree()
        # if tree is None: return False
        # return tree.bl_idname == "an_AnimationNodeTree"

        if context.area.type == "NODE_EDITOR":
            if context.area.ui_type == "an_AnimationNodeTree":
                return True

    def draw(self, context):
        winman = context.window_manager
        layout = self.layout

        layout.template_list("ANTEMPLATES_UL_panel_ui_list", "", winman, "an_templates_nodetrees", winman.an_templates_properties, "nodetrees_index", rows = 3)


        idx = winman.an_templates_properties.nodetrees_index

        if idx in range(0, len(winman.an_templates_nodetrees)):
            active_nodetree = winman.an_templates_nodetrees[winman.an_templates_properties.nodetrees_index]
            
            col = layout.column(align=True)

            col.label(text=active_nodetree.description)
            col.label(text=active_nodetree.blender_version)
            col.label(text=active_nodetree.an_version)
            col.label(text=active_nodetree.category)
            col.label(text=active_nodetree.tags)
            col.label(text=active_nodetree.hash)
            col.label(text=active_nodetree.file_url)


    # @classmethod
    # def getTree(cls):
    #     return bpy.context.space_data.edit_tree
