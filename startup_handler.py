import bpy
from bpy.app.handlers import persistent

from .internet_functions import download_file, is_connected
from .json_functions import set_nodetrees_from_json, set_properties_from_json


url = r"https://raw.githubusercontent.com/samytichadou/an_template_test/master/misc_dev/test.json"
filepath = r"C:\Users\tonton\Desktop\aaaa\test.json"

### HANDLER ###
@persistent
def antStartupHandler(scene):
    
    print() #debug
    print("AN Templates") #debug
    print() #debug

    if not is_connected():
        print("No Internet connection") #debug
        # raise error message TODO
    else:
        print("Internet connection") #debug

        print("Downloading manifest") #debug
        download_file(url, filepath)

        print("Loading manifest") #debug
        set_nodetrees_from_json(filepath)
        set_properties_from_json(filepath)