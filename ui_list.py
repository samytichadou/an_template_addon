import bpy


# topbar function
def topbar_menu_function(self, context):
    self.layout.separator()
    self.layout.popover(panel='CATHIDE_PT_panel')


class ANTEMPLATES_UL_panel_ui_list(bpy.types.UIList):

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

    # # Called once to filter/reorder items.
    # def filter_items(self, context, data, propname):

    #     helper_funcs = bpy.types.UI_UL_list

    #     display = context.window_manager.bpm_generalsettings.panel_asset_display

    #     # Default return values.
    #     flt_flags = []
    #     flt_neworder = []

    #     col = getattr(data, propname)
        
    #     ### FILTERING ###
    #     if self.filter_name or display != "ALL" or self.use_filter_sort_alpha:
    #         flt_flags = [self.bitflag_filter_item] * len(col)

    #         # name search
    #         if self.filter_name :
    #             flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, col, "name", flags=None, reverse=False)

    #         # category search
    #         if display != "ALL":
    #             for idx, asset in enumerate(col):
    #                 if asset.asset_type != display:
    #                     flt_flags[idx] = 0

    #         # Reorder by name
    #         if self.use_filter_sort_alpha:
    #             flt_neworder = helper_funcs.sort_items_by_name(col, "name")

    #     return flt_flags, flt_neworder