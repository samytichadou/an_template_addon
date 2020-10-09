import bpy


guidelines = [
    "Please fill all the fields carefully",
    "",
    "Keep the blend file as lighter as possible",
    "by removing all useless datas",
    "The blend file size must be under 25MB",
    "",
    'Remove the "Always" parameter in Auto Execution',
    "Use subprograms for better organization",
    'If possible, use a Master Subprogram for reusability',
    "Keep your nodetree readable",
    "",
    "Try to use existing tags",
    "",
    "If you don't select an image,",
    "a screenshot of the opened blend will be taken",
    "",
    "If possible, put a valid email for further exchanges",
    "It will never be public",
            ]

# submission guidelines
class ANTEMPLATES_OT_submission_guidelines(bpy.types.Operator):
    """Please Read Submission Guidelines Before Submitting a Nodetree"""
    bl_idname = "antemplates.submission_guidelines"
    bl_label = "Submission Guidelines"
    bl_options = {'REGISTER', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        return True


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):

        layout = self.layout

        col = layout.column(align=True)

        for l in guidelines:
            if l == "":
                col.separator()
            else:
                col.label(text=l)


    def execute(self, context):
        return {'FINISHED'}