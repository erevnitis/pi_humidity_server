# Purpose
Provision a Raspberry Pi4 with the tools necessary to record humidity and display historical humidity via a web interface  

# Overview
The complete process is as follows:
- Flash an SD card with Ubuntu Server 20.04
- Update Ubuntu Server
- Copy an SSH key from your device to the Pi
- Run the main_push.yml playbook

## Requirements
This project has been tested on a Raspberry Pi3 and Raspberry Pi4  
In this project I am using a BME 680 sensor for the humidity readings  
I've successfully used the BME 280 and may publish another playbook for that sensor in the future
## Variables 
Users of this repository will have to add thier own:
- sender_email, receiver_email, email password <- for email notifications of low humidity  
- SSH key
- zip code
- openweathermap API key

These can all be configured in vars/default.yml
# Project Steps
## Prepare the Raspberry Pi
Download Ubuntu Server on the Pi  
Here is a tutorial from Canonical [Install Ubuntu Server on the Pi](https://ubuntu.com/tutorials/how-to-install-ubuntu-on-your-raspberry-pi#1-overview) which lays-out all the steps needed.  
It is important to add a file named 'ssh' to the boot partition to SSH into the device  
After the SD card is formatted and Ubuntu Server is installed, insert the SD card into the Pi, connect an ethernet cable and power the Pi on.
## Determine the IP Address
There are many ways to determine the IP address of the Pi
I find mine with the help of my DHCP server on my pfSense firewall
When you find the IP address you can SSH into the device-this example uses the address of 192.168.1.11:
```bash
SSH ubunut@192.168.1.11
```
When prompted, the password is 'ubuntu'  
The first time you log into the device, Ubuntu requres a password change from the default.  
Complete the process of changing the default password and log in again to the Pi  

## Update the OS and configure the Pi
After logging back into the Pi, update the OS
```bash
sudo apt update && sudo apt dist-upgrade -y && sudo apt autoremove -y && sudo apt clean -y
```
I have found it is best to do this step before running the playbook because of the possibility of:
## A Possible Issue you may Encounter
If you see this:
```
Waiting for cache lock: Could not get lock /var/........etc
```
While the Pi is trying to update, Ubunutu may be updating in the background.  There are a few ways to fix this but one that works every time is to wait until that process is finished and restart the boostrap.sh script.  I have seen this take as long as 15 minutes-it is usually closer to 10 though.  

## Copy SSH key to Pi
To have Ansible easily connect to the Pi, copy your SSH public key to the Pi:
```bash
SSH-copy-id -i (some_SSH_key.pub) ubuntu@192.168.1.11 
```
# Clone the Repository
To clone the repository you will need Git on your machine.  
Here is a link to the instructions on how to install Git [Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)  

To clone the repository to your local machine:
```bash
git clone git@github.com:erevnitis/pi_humidity_server.git
```
This will place all the necessary files on your local machine

## Run main_push.py
The playbook should configure and install all the items necessary for the project.  
To run the playbook, navigate to the pi_humidity_server directory on your device
```bash
ansible-playbook main_push.py
```
The Pi will reboot at the end of the playbook to complete all of necessary changes. 

# Connect the BME680 Sensor to the GPIO pins on the Pi
To connect the sensor to the Pi follow this diagram:

![BME680 Wiring](files/bme680_wiring.png)

## Create the first entry in the database
Reconnect to the Pi as it was rebooted at then end of the playbook:  
```bash
ssh ansible@192.168.1.11
```

The Pi has been configured to populate the database by taking readings every 20 minutes via cron but you can test the python script immediately and create the first database entry:

```bash
python3 humidity_ansible.py
```
# Create initial graphs
The Pi has been configured to create a graph each hour to display on the webpage.  
To create the first one:
```bash
python3 create_portrait_graph.py
```
and:
```bash
python3 import_mysql_to_matplotlib.py
```
# Configure the database
If you need to make adjustments to the database you can use phpMyAdmin  
Navigate to the device IP address and '/phpmyadmin' for the homepage  
In this case it's at 192.168.1.11/phpmyadmin and here's what you should see:

![phpmyadmin_login_page](files/phpmyadmin.png)
username is 'ansible'  
password is 'khtelemacher'  

# View webpage
For the webpages to be displayed we need to tell Flask to start the service.  

Navigate to the flask directory:
```bash
cd ~/flask
```
Start the webserver:
```bash
python3 main_flask.py
```
Using a browser navigate to the Pi's IP address and port 5000  
In this example 192.168.1.11:5000 and we should see this:

![flask_main_page](files/flask_main_page.png) 