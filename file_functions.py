import os
import shutil


from .global_variables import addon_print_prefix, manifest_file


# create directory
def create_directory(filepath):
    try:
        os.makedirs(filepath)
    except OSError:
        #print (addon_print_prefix + "Creation of the directory %s failed" % filepath) #debug
        return False
    else:
        #print (addon_print_prefix + "Successfully created the directory %s " % filepath) #debug
        return True


