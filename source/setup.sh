#!/bin/bash

python3 tools/get_ip_hostname.py

chmod +x tools/*

ip=`cat ip`
rm ip
hostname=`cat hostname`
rm hostname
answer=True
confirm_ip=Y
confirm_hostname=Y
secure=N

sudo cp tools/resources/pxe-director.service /etc/systemd/system

if test -e 'tools/answer_file.yaml'
then
  if [[ $pass_along == 'True' ]]
  then
    echo In answer file setup!
  else
    echo Using answer file
    cd tools
    python3 ./answer_file.py
    chmod +x auto_setup.sh
    ./auto_setup.sh
    exit
  fi
else
  echo Is $ip your IP? Y/n
  read confirm_ip
  echo Is $hostname your hostname? Y/n
  read confirm_hostname
  echo Should we secure it "(Warning this will disable SSH after a restart)" y/N
  read secure
fi

if [[ $confirm_hostname == 'n' ]] || [[ $confirm_hostname == 'N' ]]
then
  echo What is the IP
  read ip
fi

if [[ $confirm_ip == 'n' ]] || [[ $confirm_ip == 'N' ]]
then
  echo What is the hostname
  read hostname
fi

python3 tools/setup_install.py
sudo bash tools/install_packges.sh

#python3 answer_file.py

sudo mkdir /etc/pxe-director
sudo useradd -M pxe-director

sudo cp -R web-server /etc/pxe-director

sudo chown pxe-director.pxe-director -R /etc/pxe-director
sudo firewall-cmd --reload

export secure
./tools/secure.sh

sudo systemctl enable pxe-director
sudo systemctl start pxe-director
sudo systemctl enable tftp
sudo systemctl start tftp

cd tools
./tools/install-pxe.sh

echo $ip>toolsresourcesip
mv toolsresourcesip ip
mv ip tools\resources\ip