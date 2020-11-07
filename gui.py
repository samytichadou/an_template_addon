import bpy


from .op_create_manifest import get_separated_tags
from .addon_prefs import get_addon_preferences
from .string_formatting_functions import split_string_on_spaces


class ANTEMPLATES_PT_templates_panel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_templates_panel"
    bl_label = "Templates"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Templates"


    @classmethod
    def poll(cls, context):
        if context.area.ui_type == "an_AnimationNodeTree":
            return True


    def draw(self, context):

        winman = context.window_manager
        properties_coll = winman.an_templates_properties

        layout = self.layout

        # check if nodetree available
        if not winman.an_templates_nodetrees:
            layout.label(text="No Available Templates", icon="ERROR")
            return

        col = layout.column(align=True)

        row = col.row(align=True)
        row.prop(properties_coll, "nodetree_search", text="", icon='VIEWZOOM')
        row.prop(properties_coll, "nodetree_tag_search", text="", icon='STYLUS_PRESSURE')
        row.operator("antemplates.search_tag_menu_caller", text="", icon="PLUS")
        col.prop(properties_coll, "nodetree_categories_enum", text="", icon="FILE_FOLDER")
        col.template_list("ANTEMPLATES_UL_panel_ui_list", "", winman, "an_templates_nodetrees", properties_coll, "nodetrees_index", rows = 5)

        row = layout.row(align=True)

        row.operator("antemplates.import_nodetree", text="", icon="IMPORT")

        row.separator()

        row.label(text="", icon="URL")

        row.operator('antemplates.open_url_image', text="", icon='FILE_IMAGE')
        row.operator('antemplates.open_url_video', text="", icon='FILE_MOVIE')
        row.operator('antemplates.open_url_readme', text="", icon='HELP')


class ANTEMPLATES_PT_import_options_subpanel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_import_options_subpanel"
    bl_label = "Import Options"
    bl_parent_id = "ANTEMPLATES_PT_templates_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}


    @classmethod
    def poll(cls, context):
        if context.window_manager.an_templates_nodetrees:
            return True


    def draw(self, context):

        winman = context.window_manager
        properties_coll = winman.an_templates_properties

        layout = self.layout

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


class ANTEMPLATES_PT_nodetree_infos_subpanel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_nodetree_infos_subpanel"
    bl_label = "Nodetree Infos"
    bl_parent_id = "ANTEMPLATES_PT_templates_panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}


    @classmethod
    def poll(cls, context):
        if context.window_manager.an_templates_nodetrees:
            return True


    def draw(self, context):

        winman = context.window_manager

        layout = self.layout
        
        idx = winman.an_templates_properties.nodetrees_index

        if idx in range(0, len(winman.an_templates_nodetrees)):
            active_nodetree = winman.an_templates_nodetrees[idx]
            
            col = layout.column(align=True)

            col.label(text=active_nodetree.description, icon="INFO")
            col.label(text=active_nodetree.blender_version, icon="BLENDER")
            col.label(text=active_nodetree.an_version, icon="ONIONSKIN_ON")
            col.label(text=active_nodetree.category, icon="FILE_FOLDER")
            # col.label(text=active_nodetree.hash, icon="RNA")
            # col.label(text=active_nodetree.file_url, icon="URL")
            
            col.label(text="Tags :", icon="VIEWZOOM")
            limit = 3
            ct = 0
            tag_reformat = ""
            for tag in get_separated_tags(active_nodetree.tags):
                tag_reformat += tag
                ct += 1
                if ct == limit:
                    col.label(text=tag_reformat)
                    tag_reformat = ""
                    ct = 0
                else:
                    tag_reformat += ", "
            if ct != 0:
                tag_reformat = tag_reformat[:-2]
                col.label(text=tag_reformat)


class ANTEMPLATES_PT_news_panel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_news_panel"
    bl_label = "News"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Templates"


    @classmethod
    def poll(cls, context):
        if context.area.ui_type == "an_AnimationNodeTree":
            return True


    def draw(self, context):

        properties_coll = context.window_manager.an_templates_properties

        active_news = properties_coll.news[properties_coll.active_news]

        count = str(properties_coll.active_news + 1) + "/" + str(len(properties_coll.news))

        layout = self.layout

        row = layout.row(align=True)
        row.label(text=count)
        row.operator("antemplates.newsfeed_actions", text="", icon="TRIA_LEFT").action = "PREV"
        row.operator("antemplates.newsfeed_actions", text="", icon="TRIA_RIGHT").action = "NEXT"
        
        col = layout.column(align=True)

        for line in split_string_on_spaces(active_news.name, 25):
            col.label(text=line)

        col.separator()

        if active_news.url != "":
            col.operator("antemplates.open_url", text="URL", icon="URL").url = active_news.url

        if active_news.nodetree_name != "":
            col.operator("antemplates.search_select_nodetree", text="Select", icon="RESTRICT_SELECT_OFF").name = active_news.nodetree_name
            col.operator("antemplates.import_nodetree", text="Import", icon="IMPORT").from_name = active_news.nodetree_name


class ANTEMPLATES_PT_utilities_panel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_utilities_panel"
    bl_label = "Utilities"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Templates"


    @classmethod
    def poll(cls, context):
        if context.area.ui_type == "an_AnimationNodeTree":
            return True


    def draw(self, context):

        layout = self.layout

        layout.operator("antemplates.refresh_templates", icon="FILE_REFRESH")
        layout.operator("antemplates.clear_downloads", icon="TRASH")
        layout.operator("antemplates.refresh_addon_version", icon="FILE_SCRIPT")


class ANTEMPLATES_PT_submission_panel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_submission_panel"
    bl_label = "Submission"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Templates"


    @classmethod
    def poll(cls, context):
        if context.area.ui_type == "an_AnimationNodeTree":
            return True


    def draw(self, context):

        properties_coll = context.window_manager.an_templates_properties

        layout = self.layout

        col = layout.column(align=True)
        col.label(text="Please Read the Guidelines")
        col.operator("antemplates.submission_guidelines", text="Guidelines", icon="INFO")

        col.separator()

        col.prop(properties_coll, "submission_nodetree", text="", icon="NODETREE")
        col.prop(properties_coll, "submission_category", text="", icon="FILE_FOLDER")
        col.prop(properties_coll, "submission_readme", text="")

        col.separator()

        row = col.row(align=True)
        row.prop(properties_coll, "submission_tags", text="Tags")
        row.operator("antemplates.add_tag_menu_caller", text="", icon="PLUS")

        col.separator()

        col.prop(properties_coll, "submission_small_description", text="Infos")
        
        col.prop(properties_coll, "submission_author_mail", text="Mail")
        col.prop(properties_coll, "submission_author_name", text="Name")
        
        col.separator()

        col.label(text="Optional :")

        col.prop(properties_coll, "submission_image_preview_url", text="Image")
        col.prop(properties_coll, "submission_video_preview_url", text="Video")
        col.prop(properties_coll, "submission_side_notes", text="Notes")

        layout.operator("antemplates.submit_template")


class ANTEMPLATES_PT_updater_subpanel(bpy.types.Panel):
    bl_idname = "ANTEMPLATES_PT_updater_subpanel"
    bl_label = "Addon Update"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_parent_id = "ANTEMPLATES_PT_utilities_panel"


    @classmethod
    def poll(cls, context):
        if context.window_manager.an_templates_properties.update_needed:
            return True


    def draw_header(self, context):

        self.layout.label(text="", icon="INFO")


    def draw(self, context):

        properties_coll = context.window_manager.an_templates_properties

        layout = self.layout
        
        layout.operator("antemplates.open_url", text="Download", icon="IMPORT").url=properties_coll.update_download_url

        col = layout.column(align=True)
        col.label(text=properties_coll.update_message)
        col.label(text="Remove Previous Before Installing", icon="ERROR")