#!/bin/bash
#Opening ports
sudo firewall-cmd --add-service=tftp    --permanent
sudo firewall-cmd --add-service=http    --permanent
sudo firewall-cmd --add-service=https   --permanent
sudo firewall-cmd --add-port=8080/tcp   --permanent
sudo firewall-cmd --add-port=8443/tcp   --permanent

#Reloads firewall
sudo firewall-cmd --reload

#Closing ports
if [[ $secure == 'y' ]] || [[ $secure == 'Y' ]]
then
  sudo firewall-cmd --remove-protocol=ssh --permanent
else
  echo Not removing any ports
fi

#Temp when I learn SE Linux
sudo sed -i.bak 's/^.*\SELINUX=enforcing\b.*$/SELINUX=permissive/' /etc/selinux/config
sudo setenforce 0