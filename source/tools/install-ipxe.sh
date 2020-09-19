#!/bin/bash
./get_ip_hostname.py
./ipxe_script_generator.py
cp ipxe-script.ipxe ../../dependencies/ipxe/src/
cd ../../dependencies/ipxe/src/
make EMBED=ipxe-script.ipxe
cd bin
sudo mv undionly.kpxe /var/lib/tftpboot
sudo chown nobody.nobody /var/lib/tftpboot/undionly.kpxe
