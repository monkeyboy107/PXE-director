#!/bin/python3
template = 'resources/ipxe.template'
ip_file = 'ip'
ip_template_name = 'ip'
ipxe_script = 'ipxe-script.ipxe'

with open(ip_file, 'r') as data:
    ip = data.read()

with open(template, 'r') as data:
    line = data.read().replace(ip_template_name, ip)

with open(ipxe_script, 'w+') as data:
    data.write(line)