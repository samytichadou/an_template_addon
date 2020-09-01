import os


# create directory
def create_directory(filepath):
    try:
        os.mkdir(filepath)
    except OSError:
        print ("Creation of the directory %s failed" % filepath)
        return False
    else:
        print ("Successfully created the directory %s " % filepath)
        return True