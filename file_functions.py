import os
import shutil


# create directory
def create_directory(filepath):
    try:
        os.mkdir(filepath)
    except OSError:
        print ("Creation of the directory %s failed" % filepath) #debug
        return False
    else:
        print ("Successfully created the directory %s " % filepath) #debug
        return True


# empty directory
def empty_directory(filepath):
    # delete folder
    shutil.rmtree(filepath, ignore_errors=False, onerror=None)

    # create folder
    create_directory(filepath)

    print ("Successfully emptied %s " % filepath) #debug