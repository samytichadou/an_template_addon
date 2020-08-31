import bpy


class ANTEMPLATES_PT_panel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_auto_execution_panel"
    bl_label = "Templates"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Templates"

    @classmethod
    def poll(cls, context):
        tree = cls.getTree()
        if tree is None: return False
        return tree.bl_idname == "an_AnimationNodeTree"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Placeholder")

    @classmethod
    def getTree(cls):
        return bpy.context.space_data.edit_tree
