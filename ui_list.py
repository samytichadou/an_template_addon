import bpy


def get_blender_versions_callback(scene, context):

    items = []

    items.append(("ALL", "All", ""))

    for i in context.window_manager.an_templates_properties.blender_versions:
        items.append((i.name, i.name, ""))

    return items


def get_an_versions_callback(scene, context):

    items = []

    items.append(("ALL", "All", ""))

    for i in context.window_manager.an_templates_properties.an_versions:
        items.append((i.name, i.name, ""))

    return items


def get_categories_callback(scene, context):

    items = []

    items.append(("ALL", "All", ""))

    for i in context.window_manager.an_templates_properties.categories:
        items.append((i.name, i.name, ""))

    return items


class ANTEMPLATES_UL_panel_ui_list(bpy.types.UIList):


    nodetree_blender_versions_enum : bpy.props.EnumProperty(name="Blender Versions", items = get_blender_versions_callback)
    nodetree_an_versions_enum : bpy.props.EnumProperty(name="Animation Nodes Versions", items = get_an_versions_callback)
    nodetree_categories_enum : bpy.props.EnumProperty(name="Categories", items = get_categories_callback)


    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            layout.label(text = item.name)
            row = layout.row(align=True)
            row.operator('antemplates.open_url', text='', icon='IMAGE').url = item.image_preview_url
            row.operator('antemplates.open_url', text='', icon='FILE_MOVIE').url = item.video_preview_url
            row.operator('antemplates.open_url', text='', icon='HELP').url = item.readme_url
            
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.label(text = item.name)
            row = layout.row(align=True)
            row.operator('antemplates.open_url', text='', icon='IMAGE').url = item.image_preview_url
            row.operator('antemplates.open_url', text='', icon='FILE_MOVIE').url = item.video_preview_url
            row.operator('antemplates.open_url', text='', icon='HELP').url = item.readme_url


    def draw_filter(self, context, layout):

        col = layout.column(align=True)

        row = col.row(align=True)

        if self.use_filter_invert:
            icon="ZOOM_OUT"
        else:
            icon="ZOOM_IN"
        row.prop(self, "use_filter_invert", text="", icon=icon)

        row.separator()
        row.prop(self, "use_filter_sort_alpha", text="", icon="SORTALPHA")

        if self.use_filter_sort_reverse:
            icon="SORT_DESC"
        else:
            icon="SORT_ASC"
        row.prop(self, "use_filter_sort_reverse", text="", icon=icon)

        col.prop(self, "nodetree_categories_enum",text="", icon="BLENDER")
        col.prop(self, "nodetree_blender_versions_enum", text="", icon="ONIONSKIN_ON")
        col.prop(self, "nodetree_an_versions_enum", text="", icon="FILE_FOLDER")


    # Called once to filter/reorder items.
    def filter_items(self, context, data, propname):

        helper_funcs = bpy.types.UI_UL_list

        search = context.window_manager.an_templates_properties.nodetree_search
        category = self.nodetree_categories_enum
        blender_version = self.nodetree_blender_versions_enum
        an_version = self.nodetree_an_versions_enum

        # Default return values.
        flt_flags = []
        flt_neworder = []

        col = getattr(data, propname)
        
        ### FILTERING ###
        if search or category!= "ALL" or blender_version!="ALL" or an_version!="ALL" or self.use_filter_sort_alpha:
            flt_flags = [self.bitflag_filter_item] * len(col)

            # name search
            if search :
                flt_flags = helper_funcs.filter_items_by_name(search, self.bitflag_filter_item, col, "name", flags=None, reverse=False)

            # category search
            if category != "ALL":
                for idx, item in enumerate(col):
                    if item.category != category:
                        flt_flags[idx] = 0

            # blender version search
            if blender_version != "ALL":
                for idx, item in enumerate(col):
                    if item.blender_version != blender_version:
                        flt_flags[idx] = 0

            # category search
            if an_version != "ALL":
                for idx, item in enumerate(col):
                    if item.an_version != an_version:
                        flt_flags[idx] = 0

            # Reorder by name
            if self.use_filter_sort_alpha:
                flt_neworder = helper_funcs.sort_items_by_name(col, "name")

        return flt_flags, flt_neworder