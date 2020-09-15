'''
Copyright (C) 2018 Samy Tichadou (tonton)
samytichadou@gmail.com

Created by Samy Tichadou (tonton)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {  
 "name": "AN templates",  
 "author": "Samy Tichadou (tonton)",  
 "version": (0, 1, 0),  
 "blender": (2, 83, 5), 
 "location": "",  
 "description": "",  
 "wiki_url": "",  
 "tracker_url": "",
 "category": "Node",
 "warning": "Beta version, use at your own risks"
 }


import bpy

# auto-updater
from . import addon_updater_ops


# IMPORT SPECIFICS
##################################

from .startup_handler import ant_startup_handler

from .properties import *

from .op_open_url import ANTEMPLATES_OT_open_url, ANTEMPLATES_OT_open_url_image, ANTEMPLATES_OT_open_url_video, ANTEMPLATES_OT_open_url_readme
from .op_empty_download_dir import ANTEMPLATES_OT_clear_downloads
from .op_create_manifest import ANTEMPLATES_OT_create_manifest
from .op_create_nodetree_info import ANTEMPLATES_OT_create_nodetree_info
from .op_edit_nodetree_info import ANTEMPLATES_OT_edit_nodetree_info
from .op_import_nodetree import ANTEMPLATES_OT_import_nodetree
from .op_tag_search import ANTEMPLATES_MT_search_tag_menu, ANTEMPLATES_OT_search_tag_menu_caller, ANTEMPLATES_OT_search_tag
from .op_tag_add import ANTEMPLATES_MT_add_tag_menu, ANTEMPLATES_OT_add_tag_menu_caller, ANTEMPLATES_OT_add_tag
from .op_refresh_templates import ANTEMPLATES_OT_refresh_templates
from .op_submit_template import ANTEMPLATES_OT_submit_template

from .gui import ANTEMPLATES_PT_templates_panel, ANTEMPLATES_PT_import_options_subpanel, ANTEMPLATES_PT_nodetree_infos_subpanel, ANTEMPLATES_PT_utilities_panel, ANTEMPLATES_PT_submission_panel
from .ui_list import ANTEMPLATES_UL_panel_ui_list

from .addon_prefs import ANTEMPLATESAddonPrefs

# register
##################################

classes = (
            ANTemplatesNodetrees,
            ANTemplatesBlenderVersions,
            ANTemplatesANVersions,
            ANTemplatesCategories,
            ANTemplatesTags,
            ANTemplatesProperties,

            ANTEMPLATES_OT_open_url,
            ANTEMPLATES_OT_open_url_image,
            ANTEMPLATES_OT_open_url_video,
            ANTEMPLATES_OT_open_url_readme,
            ANTEMPLATES_OT_clear_downloads,
            ANTEMPLATES_OT_create_manifest,
            ANTEMPLATES_OT_create_nodetree_info,
            ANTEMPLATES_OT_edit_nodetree_info,
            ANTEMPLATES_OT_import_nodetree,
            ANTEMPLATES_MT_search_tag_menu,
            ANTEMPLATES_OT_search_tag_menu_caller,
            ANTEMPLATES_OT_search_tag,
            ANTEMPLATES_MT_add_tag_menu,
            ANTEMPLATES_OT_add_tag_menu_caller,
            ANTEMPLATES_OT_add_tag,
            ANTEMPLATES_OT_refresh_templates,
            ANTEMPLATES_OT_submit_template,

            ANTEMPLATES_PT_templates_panel,
            ANTEMPLATES_PT_import_options_subpanel,
            ANTEMPLATES_PT_nodetree_infos_subpanel,
            ANTEMPLATES_PT_utilities_panel,
            ANTEMPLATES_UL_panel_ui_list,
            ANTEMPLATES_PT_submission_panel,

            ANTEMPLATESAddonPrefs,
        )

def register():

    # auto-updater
    addon_updater_ops.register(bl_info)

    ### OPERATORS ###
    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)

    ### PROPERTIES ###
    bpy.types.WindowManager.an_templates_nodetrees = \
        bpy.props.CollectionProperty(type = ANTemplatesNodetrees, name="AN Template Nodetrees")

    bpy.types.WindowManager.an_templates_properties = \
        bpy.props.PointerProperty(type = ANTemplatesProperties, name="AN Template Properties")

    ### HANDLER ###
    bpy.app.handlers.load_post.append(ant_startup_handler)


def unregister():

    # auto updater
    addon_updater_ops.unregister()
   
    ### OPERATORS ###
    from bpy.utils import unregister_class
    for cls in reversed(classes) :
        unregister_class(cls)

    ### PROPERTIES ###
    del bpy.types.WindowManager.an_templates_nodetrees
    del bpy.types.WindowManager.an_templates_properties

    ### HANDLER ###
    bpy.app.handlers.load_post.remove(ant_startup_handler)