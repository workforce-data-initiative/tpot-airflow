#!/bin/sh

export DC_VER="1.16.1"

# Install docker and run
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/$DC_VER/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
