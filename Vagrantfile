# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.provider "virtualbox" do |v|
    v.memory = 8192
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y ca-certificates curl gnupg lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io
    groupadd docker
    usermod -aG docker vagrant
    add-apt-repository ppa:deadsnakes/ppa
    apt install -y magic-wormhole git python3.9 python3-pip
    pip install pipenv
    echo "\nexport PATH=\'/home/vagrant/.local/bin:$PATH\'" >> /home/vagrant/.bashrc
    curl https://cli-assets.heroku.com/install.sh | sh
    curl -s https://install.zerotier.com | sudo bash
    zerotier-cli join 6ab565387aafde26
    cp -r /vagrant .
  SHELL
end
