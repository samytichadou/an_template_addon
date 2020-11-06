import os

from .addon_prefs import get_addon_preferences
from .global_variables import newsfeed_file, newsfeed_url
from .internet_functions import download_file


# reload newsfeed
def reload_newsfeed(manifest_dataset):
    newsfeed_path = os.path.join(get_addon_preferences().download_folder, newsfeed_file)

    if not os.path.isfile(newsfeed_path):
        download_file(newsfeed_url, newsfeed_path)

    return