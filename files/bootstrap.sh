#! /bin/bash
# Run this script as root: sudo su
purple='\033[1;35m'
nocolor='\033[0m'
green='\033[1;32m'
device_name="humidity_server"
username="ansible"
groupname="wheel"
ssh_dir="/home/$username/.ssh"
sudo_permissions="$username ALL=(ALL) NOPASSWD: ALL"
ssh_key="insert ssh key here"
pass=$(perl -e 'print crypt($ARGV[0], "password")' hktelemacher)

echo -e "${purple}\n\nSet the timezone\n\n${nocolor}"
timedatectl set-timezone "America/Detroit"
echo $(timedatectl)

echo -e "${purple}\n\nI'm going to update the OS now.....\n\n${nocolor}"
sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y && sudo apt clean -y

echo -e "${purple}\n\nChange hostname in hostname file\n\n${nocolor}"
sed -i "s/raspberry/$device_name/" /etc/hostname
echo -e "${green}\n\n.....Hostname changed to $device_name in hostname file....\n\n${nocolor}"

echo -e "${purple}\n\nChange hostname in hosts file\n\n${nocolor}"
sed -i "s/raspberry/$device_name/" /etc/hosts
echo -e "${green}\n\n.....Hostname changed to $device_name in hosts file....\n\n${nocolor}"

echo -e "${purple}\n\nAdd group $groupname\n\n${nocolor}"
sudo groupadd $groupname
echo -e "${green}\n\n.....Added the group $groupname....\n\n${nocolor}"

echo -e "${purple}\n\nAdd user\n\n${nocolor}"
useradd -m -p $pass $username -s /bin/bash -g $groupname -G adm,sudo
echo -e "${green}\n\n.....Added the user $username....\n\n${nocolor}"

echo -e "${purple}Add sudo permissions for $username\n\n${nocolor}"
echo $sudo_permissions > /etc/sudoers.d/$username
echo -e "${green}\n\n.....Added sudo permissions for $username....\n\n${nocolor}"

echo -e "${purple}Make .ssh directory for $username\n\n${nocolor}"
if [ -d "$ssh_dir" ]; then
echo "Directory already exists\n" ;
else
`mkdir -p $ssh_dir`;
fi
echo -e "${green}\n\n......ssh Directory Created....\n\n${nocolor}"

echo -e "${purple}Add ssh key for user${nocolor}"
echo $ssh_key > /home/$username/.ssh/authorized_keys
echo -e "${green}\n\n.....ssh key added for $username....\n\n${nocolor}"

echo -e "${purple}I'm going to restart the device now\n\n${nocolor}"
sudo reboot now