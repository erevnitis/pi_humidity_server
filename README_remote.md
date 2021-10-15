# Purpose
Provision a Raspberry Pi4 with the tools necessary to record humidity and display historical humidity via a web interface  

## Overview
The complete process is as follows:
- Flash an SD card with Ubuntu Server 20.04
- Copy and paste a "bootstrap" script to configure:
    - Timezone
    - Group
    - User
    - sudo permissions
    - ssh key
- Copy and paste another script to allow the Pi to receive the repository
- Install Apache, MySQL, PHP and configure them for this application
- Install phpMyAdmin to more easily administer the database
- Install python dependencies to allow the Pi to read the data from the BME680 sensor
- Install a Flask instance to allow for easy viewing of current and historical humidity data
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

These can all be configured in vars/default.yml
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
## Update the OS and configure the Pi
The Pi needs some parameters changed to be able to receive the playbook.
We need to copy and paste the bootstrap.sh file to a newly created file
```bash
sudo su
```
To become root
```bash
nano bootstrap.sh
``` 
To create the file we need to past into  
Copy the contents of [bootstrap.sh](files/bootstrap.sh),  
----------> Be sure to insert your ssh key into the variables <-----------  
save the file  
```bash
chmod +x bootstrap.sh
```
To make the file executable
```bash
./bootstrap.sh
```
To run the script  

## Issue #1
If you get:
```
Waiting for cache lock: Could not get lock..etc
```
Ubunut may be updating in the background.  One course of action is to wait until that proces is finished and restart the boostrap.sh script.

## Install GIT and Ansible
The last command of bootstrap.sh reboots the device  
Reconnect to the device using the new username 'ansible'
```bash
ssh ansible@192.168.1.11
```
We have one more script to cut and paste.  This will allow us to import the repository and run the playbook.  
```bash
sudo nano prepare_pi.sh
```
Creates the new file.  
Copy and paste [prepare_pi.sh](files/prepare_pi.sh)  
Save the file   
```bash
sudo chmod +x prepare_pi.sh
```
Again to make the file executable
```bash
./prepare_pi.sh
```
To run the script.  At the end, the Pi will reboot again.  
## Clone the repository
SSH into the device
```bash
ssh ansible@192.168.1.11
```
Clone the repository
```bash
git clone https://github.com/erevnitis/pi_humidity_server.git
```
## Configure variables in vars/default directory
Edit vars/default.yml
```bash
sudo nano pi_humidity_server/vars/default.yml
```
Insert:
- OpenWeatherMap API Key
- Zip Code
- Sender Email
- Receiver Email
- Email Password
- SSH Key if you're going to use the playbook to add the ssh-key  

Change directory to the repository directory
```bash
cd pi_humidity_server
```

Run the playbook
```bash
ansible-playbook main.yml
```
## Commit the changes
We've added our user 'ansible' to the group 'i2c' but without either logging out and back in or restarting the device 'ansible' is not a member of the group.  This will prevent us from reading the sensor data.  To fix this either log-out and back in again or restart the device.  

# Connect the Sensor
To connect the sensor to the Pi
![BME680 Wiring](files/bme680_wiring.png)

## Create an entry in the database
The Pi has been configured to populate the database by taking readings every 20 minutes via cron  
You can test the python script.
In the pi_humidity_server directory
```
/home/ansible/pi_humidity_server
```
```bash
python3 humidity_ansible.py
```
# Create initial graphs
The Pi has been configured to create a graph each hour to display on the webpage  
To create the first one
```bash
python3 create_portrait_graph.py
```
and
```bash
python3 import_mysql_to_matplotlib.py
```
# View webpage
Navigate to the flask directory
```
/home/ansible/flask
```
Start the webserver
```bash
python3 main_flask.py
```
Using a browser navigate to the Pi's IP address and port 5000  
In this example 192.168.1.11:5000 and we should see this:
![flask_main_page](files/flask_main_page.png)
# Configure the database
If you need to make adjustments to the database you can use phpMyAdmin  
Navigate to the device IP address and /phpmyadmin for the homepage  
In this case it's at 192.168.1.11/phpmyadmin and here's what you should see:
![phpmyadmin_login_page](files/phpmyadmin.png)
username is 'ansible'  
password is 'khtelemacher'


