#!/usr/bin/env python3
import smtplib, ssl
import board
import adafruit_bme680
from variables import get_var

i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
humidity = ("{0:.1f}".format(bme680.relative_humidity))

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = get_var('sender_email')
receiver_email = get_var('receiver_email')
email_password = get_var('email_password')
message = """\
Subject: Your Humidor is Dry

You may want to add water.  Your Humidor's most recent reading was: """ + str(humidity)
#print(humidity)



context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, email_password)
    server.sendmail(sender_email, receiver_email, message)