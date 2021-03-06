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
    display_downloaded : bpy.props.BoolProperty(name="Downloaded", description="Display an icon to know if a NodeTree is available offline")


    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        icon="FILE"

        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            layout.label(text = item.name)
            if self.display_downloaded and item.downloaded:
                layout.label(text="", icon=icon)
            
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.label(text = item.name)
            if self.display_downloaded and item.downloaded:
                layout.label(text="", icon=icon)


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

        row.separator()
        row.prop(self, "display_downloaded", text="", icon="FILE")

        col.prop(self, "nodetree_blender_versions_enum", text="", icon="BLENDER")
        col.prop(self, "nodetree_an_versions_enum", text="", icon="ONIONSKIN_ON")


    # Called once to filter/reorder items.
    def filter_items(self, context, data, propname):

        helper_funcs = bpy.types.UI_UL_list

        properties_coll = context.window_manager.an_templates_properties
        search = properties_coll.nodetree_search
        tag_search = properties_coll.nodetree_tag_search
        category = properties_coll.nodetree_categories_enum
        blender_version = self.nodetree_blender_versions_enum
        an_version = self.nodetree_an_versions_enum

        # Default return values.
        flt_flags = []
        flt_neworder = []

        col = getattr(data, propname)
        
        ### FILTERING ###
        if search or category!= "ALL" or blender_version!="ALL" or an_version!="ALL" or self.use_filter_sort_alpha:
            flt_flags = [self.bitflag_filter_item] * len(col)

            # search
            if search:
                for idx, item in enumerate(col):
                    if search.lower() in item.name.lower():
                        continue
                    if tag_search:
                        chk_tag = True
                        for tag in search.lower().split("+"):
                            tag = tag.strip()
                            if tag not in item.tags.lower():
                                chk_tag = False
                                break
                        if chk_tag:
                            continue
                    #else:
                    flt_flags[idx] = 0

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