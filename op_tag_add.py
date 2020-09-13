import bpy


# search tag menu
class ANTEMPLATES_MT_add_tag_menu(bpy.types.Menu):
    bl_label = "Add Tag"
    bl_idname = "ANTEMPLATES_MT_add_tag_menu"

    def draw(self, context):
        layout = self.layout

        for t in context.window_manager.an_templates_properties.tags:
            tag_name = t.name
            op = layout.operator("antemplates.add_tag", text=tag_name)
            op.tag = tag_name


# menu caller
class ANTEMPLATES_OT_add_tag_menu_caller(bpy.types.Operator):
    """Add Specific Tag"""
    bl_idname = "antemplates.add_tag_menu_caller"
    bl_label = "Add Tag"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.wm.call_menu(name="ANTEMPLATES_MT_add_tag_menu")
        return {'FINISHED'}


# search tag operator
class ANTEMPLATES_OT_add_tag(bpy.types.Operator):
    """Add selected Tag"""
    bl_idname = "antemplates.add_tag"
    bl_label = "Add this Tag"
    bl_options = {'REGISTER', 'INTERNAL'}

    tag : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        properties_call = context.window_manager.an_templates_properties

        tag_field = properties_call.submission_tags

        if not tag_field.strip().endswith(","):
            properties_call.submission_tags += ","

        properties_call.submission_tags += self.tag

        #context.area.tag_redraw()

        return {'FINISHED'}