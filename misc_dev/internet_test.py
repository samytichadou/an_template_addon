import socket

try:
    # connect to the host -- tells us if the host is actually
    # reachable
    socket.create_connection(("1.1.1.1", 53))
    print("ok")
except OSError:
    print("nop")
    pass