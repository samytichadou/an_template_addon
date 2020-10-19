def is_connected():
    #import socket
    #try:
        # connect to the host -- tells us if the host is actually reachable
    #    socket.create_connection(("1.1.1.1", 53))
    #    return True
    #except OSError:
    #    pass
    #return False
    return True
    

def read_online_json(url):
    import requests
    
    file_object = requests.get(url)

    return file_object.json()


def download_file(url, filepath):
    import requests
    
    file_object = requests.get(url)
    
    with open(filepath, 'wb') as local_file:
        local_file.write(file_object.content)
