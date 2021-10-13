#! /bin/bash

purple='\033[1;35m'
nocolor='\033[0m'
green='\033[1;32m'

echo -e "${purple}Updating system\n\n${nocolor}"
sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y && sudo apt clean -y
echo -e "${green}\n\n.....We're up to date....\n\n${nocolor}"

echo -e "${purple}Install GIT\n\n${nocolor}"
sudo apt install git -y
echo -e "${green}\n\n.....GIT is installed....\n\n${nocolor}"

echo -e "${purple}Install Ansible Dependencies\n\n${nocolor}"
sudo apt install python3-pip python-dev -y
echo -e "${green}\n\n.....Ansible Dependencies are Installed....\n\n${nocolor}"

echo -e "${purple}Install Ansible using pip\n\n${nocolor}"
sudo python3 -m pip install Ansible
echo -e "${green}\n\n.....Anisble is installed....\n\n${nocolor}"

echo -e "${purple}I'm going to reboot the device now\n\n${nocolor}"
sudo reboot now