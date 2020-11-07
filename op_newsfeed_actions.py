import bpy


class ANTEMPLATES_OT_newsfeed_actions(bpy.types.Operator):
    bl_idname = "antemplates.newsfeed_actions"
    bl_label = "Newsfeed Actions"
    bl_description = "Go to Previous/Next News"
    bl_options = {'REGISTER', 'INTERNAL'}

    action: bpy.props.EnumProperty(
        items=(
            ('PREV', "Previous", ""),
            ('NEXT', "Next", ""),
            )
        )


    @classmethod
    def poll(cls, context):
        return len(context.window_manager.an_templates_properties.news) not in {0,1}


    def invoke(self, context, event):

        properties_coll = context.window_manager.an_templates_properties

        idx = properties_coll.active_news
        total = len(properties_coll.news)

        if self.action == 'PREV':
            if idx - 1 in range(0, total):
                context.window_manager.an_templates_properties.active_news -= 1
            else:
                context.window_manager.an_templates_properties.active_news = total - 1
        else:
            if idx + 1 in range(0, total):
                context.window_manager.an_templates_properties.active_news += 1
            else:
                context.window_manager.an_templates_properties.active_news = 0

        return {"FINISHED"}