#!/usr/bin/env python3
#This is a script to take data from a bme680 sensor, send it to a database 
# on a RaspberryPi so historical data can be viewed
# There is a guide John_Humidor.odt which states the steps used to do this

import requests, json
import configparser
from time import sleep
import board
import busio
import adafruit_bme680
import mysql.connector
from mysql.connector import errorcode
import smtplib, ssl
from variables import get_var

# Variables
mysql_username = get_var('mysql_username')
mysql_password = get_var('mysql_password')
zip_code = get_var('zip_code')
api_key = get_var('api_key')
api_url = "http://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
r = requests.get(api_url)
json_response = r.json()
weather_data = json.dumps(r.json())
current_pressure = json_response["main"]["pressure"]
outside_humidity = json_response["main"]["humidity"]

# Create library object using our Bus I2C port
i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# OR create library object using our Bus SPI port
# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# bme_cs = digitalio.DigitalInOut(board.D10)
# bme680 = adafruit_bme680.Adafruit_bme680_SPI(spi, bme_cs)

# Value (current Sea Level Pressure) grabbed from openweathermap
bme680.sea_level_pressure = current_pressure
#Values changed to a readable form I'm used to 
temperature = (bme680.temperature *(9/5) + 32)
inside_humidity = bme680.relative_humidity
pressure = (bme680.pressure * .02953)
altitude = (bme680.altitude * 3.28084)

#This is to send an email when the humidity in the humidor gets below a predetermined value
if inside_humidity < 60 and inside_humidity > 0:
    try:
      import testemail.py
    except:
      pass

print("\nTemperature: %0.1f F" % temperature)
print("Inside Humidity: %0.1f %%" % inside_humidity)
print("Outside Humidity: %0.1f %%" % outside_humidity)
print("Pressure: %0.1f inHg" % pressure)
print("Altitude = %0.2f feet" % altitude)

#Send data to the mysql server located on the pi set-up as a server
try:
  cnx = mysql.connector.connect(user=mysql_username, password=mysql_password, host='127.0.0.1', database='humidity')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
cursor = cnx.cursor()
cursor.execute("INSERT INTO bme680_tbl (temperature, inside_humidity, outside_humidity) VALUES (%s, %s, %s)", (temperature, inside_humidity, outside_humidity))
cnx.commit()
sleep(2)
cnx.close()
print("Add Another One Johnnie!")