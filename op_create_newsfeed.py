import bpy
import os


from .json_functions import create_json_file, read_json
from .op_create_manifest import generate_hash
from .print_functions import print_and_report
from .addon_prefs import get_addon_preferences


class ANTEMPLATES_OT_news_temp_actions(bpy.types.Operator):
    bl_idname = "antemplates.news_temp_actions"
    bl_label = "News Actions"
    bl_description = "Temporary News Actions"

    action: bpy.props.EnumProperty(
        items=(
            ('ADD', "Add", ""),
            ('DEL', "Delete", ""),
            )
        )
    index: bpy.props.IntProperty()

    def invoke(self, context, event):

        temp_news = context.window_manager.an_templates_properties.temp_news

        if self.action == 'ADD':
            temp_news.add()
        else:
            temp_news.remove(self.index)

        return {"FINISHED"}


class ANTEMPLATES_OT_create_newsfeed(bpy.types.Operator):
    """Create or Edit Newsfeed File"""
    bl_idname = "antemplates.create_newsfeed"
    bl_label = "Create Newsfeed"
    bl_options = {'REGISTER', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        newsfeed_filepath = get_addon_preferences().output_newsfeed_file
        if newsfeed_filepath != "":
            return not os.path.isdir(bpy.path.abspath(newsfeed_filepath))


    def invoke(self, context, event):
        newsfeed_filepath = get_addon_preferences().output_newsfeed_file
        temp_news = context.window_manager.an_templates_properties.temp_news

        if os.path.isfile(newsfeed_filepath):
            datas = read_json(newsfeed_filepath)
            for n in datas["news"]:
                new_news = temp_news.add()
                new_news.name = n["name"]
                new_news.url = n["url"]
                new_news.nodetree_name = n["nodetree_name"]
                
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        temp_news = context.window_manager.an_templates_properties.temp_news

        layout = self.layout

        idx = 0
        for n in temp_news:
            col = layout.column(align=True)
            row = col.row(align=True)
            row.prop(n, "name", text="", icon="HELP")
            op = row.operator("antemplates.news_temp_actions", text="", icon="X")
            op.action = "DEL"
            op.index = idx
            col.prop(n, "url", text="", icon="URL")
            col.prop(n, "nodetree_name", text="", icon="NODETREE")
            idx += 1

        layout.operator("antemplates.news_temp_actions", text="Create News", icon="ADD").action = "ADD"


    def execute(self, context):

        newsfeed_filepath = get_addon_preferences().output_newsfeed_file

        winman = context.window_manager
        temp_news = winman.an_templates_properties.temp_news
        
        # check and correct output path

        json_path = bpy.path.abspath(newsfeed_filepath)

        if not os.path.isdir(os.path.dirname(json_path)):
            print_and_report(self, "Incorrect Output Path", "WARNING")
            return {'FINISHED'}

        if not json_path.endswith(".json"):
            json_path += ".json"

        # create dataset
        datas = {}

        datas["news"] = []

        for n in temp_news:
            new_news = {}
            new_news["name"] = n.name
            new_news["url"] = n.url
            new_news["nodetree_name"] = n.nodetree_name
            datas["news"].append(new_news)

        datas["newsfeed_hash"] = generate_hash(10)

        print_and_report(None, "Cleaning Temporary News Collection", "INFO") #debug
        temp_news.clear()

        print_and_report(None, "Creating Newsfeed File", "INFO") #debug

        #print(datas) #debug

        create_json_file(datas, json_path)

        print_and_report(self, "Newsfeed File Successfully Created", "INFO") #debug

        return {'FINISHED'}