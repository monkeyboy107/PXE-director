Vagrant.configure("1") do |config|
  config.vm.box = "centos/7"
  config.vm.provision "shell", inline: <<-SHELL
    sudo yum install -y git python3 pip3
    git clone https://github.com/monkeyboy107/PXE-director
    cd PXE-director
    git checkout dev
    pip3 install -r requirements.txt
#     ./venv/bin/pip-compile --output-file requirements.txt requirements.txt
    cd web
    python3 RUN-ME-FIRST-TO-SETUP --new-user admin --user-password password --regen-ssl
  SHELL