import bpy
from bpy.app.handlers import persistent

from .internet_functions import download_file, is_connected


url = r"https://raw.githubusercontent.com/samytichadou/an_template_test/master/misc_dev/test.json?token=AGIPBI6PDXT2V7V2KD4WY6K7JUG5G"
filepath = r"C:\Users\tonton\Desktop\aaaa\test.json"

### HANDLER ###
@persistent
def antStartupHandler(scene):
    
    print() #debug
    print("AN Templates") #debug
    print() #debug

    if not is_connected():
        print("No Internet connection")
        # raise error message TODO
    else:
        print("Internet connection")
        download_file(url, filepath)