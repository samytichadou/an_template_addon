import bpy
import os

from .addon_prefs import get_addon_preferences

# nodetrees
image_preview = "image_preview.png"
readme = "readme.md"
nodetree_infos = "nodetree_infos.json"

# common
addon_print_prefix = "AN Templates --- "

# file names
manifest_file = "manifest.json"
global_k_file = "global_k.json"
newsfeed_file = "newsfeed.json"

# global k
global_k_filepath = os.path.join(os.path.dirname(__file__), global_k_file)

# mail
submission_mail_subject = "Submission - "

# github libraries
an_lib_github = "https://raw.githubusercontent.com/samytichadou/animation_nodes_examples/master/library/"
manifest_url = an_lib_github + manifest_file
global_k_url = an_lib_github + global_k_file
news_feed_url = an_lib_github + newsfeed_file

addon_version_url = "https://raw.githubusercontent.com/samytichadou/an_template_addon/master/addon_version.json"