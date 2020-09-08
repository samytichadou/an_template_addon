import os
import shutil


from .global_variables import addon_print_prefix


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


# empty directory
def empty_directory(filepath):
    # delete folder
    shutil.rmtree(filepath, ignore_errors=False, onerror=None)

    # create folder
    create_directory(filepath)

    print (addon_print_prefix + "Successfully emptied %s " % filepath) #debug