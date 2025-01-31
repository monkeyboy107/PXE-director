## Credits
* Isaac Kerley

## Hacking
### Vagrant

#### Libvirt
This requires libvirt-dev/vagrant-devel and nfs-kernel-server.
```bash
export VAGRANT_DEFAULT_PROVIDER=libvirt
sudo systemctl start nfs-server
vagrant plugin install vagrant-libvirt
vagrant up
```

#### Entering the vm
```bash
vagrant ssh
```
