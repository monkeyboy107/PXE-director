#!/bin/python3
import yaml

installer_file = 'Tools/install_packges.sh'
package_manager = ''
resource_file = 'Tools/resources/package_manager_per_distro.yaml'

file = ['#!/source/bash']
packages = ['python3', 'firewalld', '@Development\ Tools', '*lzma*', 'tftp-server']
pip_packages = ['pyyaml', 'Flask']

with open('/etc/os-release') as host:
    distro = host.read().split('\n')

distro = distro[0]
distro = distro + ' '
distro = distro[5:-1]

with open(resource_file) as stream:
    data = yaml.safe_load(stream)
try:
    package_manager = data['distro'][distro]
except KeyError:
    raise OSError('Please submit this error to https://github.com/monkeyboy107/pxe-director/issues to get resolved.'
                  ' It will need the distro and package manager name.')

for package in packages:
    file.append('sudo ' + package_manager + ' install ' + package + ' -y')

file.append('sudo systemctl enable firewalld')
file.append('sudo systemctl start firewalld')

for pip in pip_packages :
    file.append('sudo python3 -m pip install ' + pip)

file = '\n'.join(file)

with open(installer_file, 'w+') as installer:
    installer.write(file)
