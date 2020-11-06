import bpy
import os

from .addon_prefs import get_addon_preferences

# nodetrees
image_preview = "image_preview.png"
readme = "readme.md"
nodetree_infos = "nodetree_infos.json"

# github libraries
manifest_url = "https://raw.githubusercontent.com/samytichadou/animation_nodes_examples/master/library/manifest.json"
global_k_url = "https://raw.githubusercontent.com/samytichadou/animation_nodes_examples/master/library/global_k.json"
addon_version_url = "https://raw.githubusercontent.com/samytichadou/an_template_addon/master/addon_version.json"

# global k
global_k_filepath = os.path.join(os.path.dirname(__file__), "global_k.json")

# common
addon_print_prefix = "AN Templates --- "

# files
manifest_file = "manifest.json"

# mail
submission_mail_subject = "Submission - "