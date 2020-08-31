import bpy
from bpy.app.handlers import persistent

import socket


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False

def download_json():
    json_adress = 
    file_path = r"C:\Users\tonton\Desktop\aaaa\test.json"
    
    import urllib.request
    urllib.request.urlretrieve(json_adress, file_path)

### HANDLER ###
@persistent
def antStartupHandler(scene):
    
    print() #debug
    print("AN Templates") #debug
    print() #debug

    if is_connected():
        print("Internet connection")
    else:
        print("No Internet connection")