def is_connected(host="8.8.8.8", port=53, timeout=3):
    import socket

    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False
    

def read_online_json(url):
    import requests
    
    file_object = requests.get(url)

    return file_object.json()


def download_file(url, filepath):
    import requests
    
    file_object = requests.get(url)
    
    with open(filepath, 'wb') as local_file:
        local_file.write(file_object.content)
