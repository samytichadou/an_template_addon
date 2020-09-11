import bpy


# search tag menu
class ANTEMPLATES_MT_search_tag_menu(bpy.types.Menu):
    bl_label = "Search Tag"
    bl_idname = "ANTEMPLATES_MT_search_tag_menu"

    def draw(self, context):
        layout = self.layout
        
        for t in context.window_manager.an_templates_properties.tags:
            tag_name = t.name
            op = layout.operator("antemplates.search_tag", text=tag_name)
            op.tag = tag_name


# menu caller
class ANTEMPLATES_OT_search_tag_menu_caller(bpy.types.Operator):
    """Search Specific Tag"""
    bl_idname = "antemplates.search_tag_menu_caller"
    bl_label = "Search Tag"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.wm.call_menu(name="ANTEMPLATES_MT_search_tag_menu")
        return {'FINISHED'}


# search tag operator
class ANTEMPLATES_OT_search_tag(bpy.types.Operator):
    """Search selected Tag"""
    bl_idname = "antemplates.search_tag"
    bl_label = "Search this Tag"
    bl_options = {'REGISTER', 'INTERNAL'}

    tag : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        properties_call = context.window_manager.an_templates_properties

        if not properties_call.nodetree_tag_search:
            properties_call.nodetree_tag_search = True

        context.window_manager.an_templates_properties.nodetree_search = self.tag

        context.area.tag_redraw()

        return {'FINISHED'}