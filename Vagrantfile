# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"
  config.vm.provider :libvirt do |domain|
    domain.driver = "qemu"
    domain.memory = 1024
    domain.cpus = 2
  end
  config.vm.synced_folder ".", "/vagrant", disabled: true
end
