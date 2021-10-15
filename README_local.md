# Overview
The complete process is as follows:
- Flash an SD card with Ubuntu Server 20.04
- Run main1.yml playbook to set the initial conditions of the Pi
- Run main2.yml playbook to install:
    - Apache, MySQL, PHP, phpMyAdmin, python dependencies, and others

## Requirements
This project has been tested on a Raspberry Pi3 and Raspberry Pi4  
In this project I am using a BME 680 sensor for the humidity readings  
I've successfully used the BME 280 and may publish another playbook for that sensor in the future
## Variables 
Users of this repository will have to add thier own:
- sender_email, receiver_email, email password <- for email notifications of low humidity  
- ssh key
- zip code
- openweathermap API key

These need to be configured in vars/default.yml
# Project Steps
## Prepare the Raspberry Pi
Download Ubuntu Server on the Pi  
Here is a tutorial from Canonical [Install Ubuntu Server on the Pi](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#1-overview)
It is important to add a file named 'ssh' to the boot partition to ssh into the device
When the SD card is formatted and Ubuntu Server is installed, insert the card, connect an ethernet cable and power the Pi on.
## Determine the IP Address
There are many ways to determine the IP address of the Pi
I find mine with the help of my DHCP server on my pfSense firewall
When you find the IP address you can ssh into the device-this example has the address as 192.168.1.11
```bash
ssh ubunut@192.168.1.11
```
When prompted, the password is 'ubuntu'  
The first time you log into the device, Ubuntu requres a password change from the default.  
Complete the process of changing the default password and log in again to the Pi  

## Update the OS and configure the Pi
After logging back into the Pi, update the OS
```bash
sudo apt update && sudo apt dist-upgrade -y && sudo apt autoremove -y && sudo apt clean -y
```
## Issue #1
If you get:
```
Waiting for cache lock: Could not get lock..etc
```
Ubuntu may be updating in the background.  One course of action is to wait until that proces is finished and restart the update.  
## Copy ssh key to Pi
To easily connect to the Pi, copy your ssh public key to the pi 
```bash
ssh-copy-id -i (some_ssh_key.pub) ubuntu@192.168.1.11 
```

## Run main1.py
Run the first playbook which will prepare the Pi to receive the remaining plays under a new user.  The playbook finishes by restarting the Pi

## Run main2.py
This second playbook runs under the new user 'ansible' and installs everything we need for our project to work.  