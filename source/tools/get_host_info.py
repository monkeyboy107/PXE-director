#!/bin/python3
import socket

def get_host():
    return socket.gethostname()

def get_ip():
    host = socket.gethostname()
    return socket.gethostbyname(host)

if __name__ == '__main__':
    print(get_ip())
    print(get_host())