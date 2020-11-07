import bpy

from .print_functions import print_and_report


class ANTEMPLATES_OT_search_select_nodetree(bpy.types.Operator):
    bl_idname = "antemplates.search_select_nodetree"
    bl_label = "Select Nodetree"
    bl_description = "Select Nodetree in Templates Panel"
    bl_options = {'REGISTER', 'INTERNAL'}

    name : bpy.props.StringProperty(default="")


    @classmethod
    def poll(cls, context):
        return True


    def execute(self, context):

        winman = context.window_manager

        properties_coll = winman.an_templates_properties
        nodetree_coll = winman.an_templates_nodetrees

        try:
            nodetree_coll[self.name]
        except KeyError:
            print_and_report(self, "Unable to Find Nodetree : " + self.from_name, "WARNING") #debug
            return {'FINISHED'}

        properties_coll.nodetree_search = self.name

        idx = 0
        for n in nodetree_coll:

            if n.name == self.name:
                properties_coll.nodetrees_index = idx
                break

            idx += 1

        print_and_report(self, "Nodetree Selected in Templates Panel", "INFO") #debug

        return {"FINISHED"}