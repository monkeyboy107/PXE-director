#!/bin/python3
import socket

ipfile = 'ip'
hostname = 'hostname'

host = socket.gethostname()
ip = socket.gethostbyname(host)

with open(ipfile, 'w+') as file:
    file.write(ip)
with open(hostname, 'w+') as file:
    file.write(host)