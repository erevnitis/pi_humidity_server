#!/usr/bin/env python3
# This is a geeksforgeeks.org tutorial on how to grab mysql data and place it in matplotlib

from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import mysql.connector
from variables import get_var

# Variables
mysql_username = get_var('mysql_username')
mysql_password = get_var('mysql_password')
default_user = get_var('default_user')

# Create a variable used to connect to the database
mydb=mysql.connector.connect(host="localhost",user=mysql_username,password=mysql_password,database="humidity")

mycursor=mydb.cursor()

# Fetch the data from the database
mycursor.execute("select ID, inside_humidity, outside_humidity from bme680_tbl")
result = mycursor.fetchall

inside_humidity = []
outside_humidity = []
id = [] # Change this to have the x-axis the date and formatted into something like 'days ago'

for i in mycursor:
    id.append(i[0])
    inside_humidity.append(i[1]) # second column
    outside_humidity.append(i[2])

# Set the Fonts
font0 = FontProperties()

# Set the size of the matplotlib canvas
plt.figure(figsize = (16,9))

# Generate the scatterplot
plt.plot(id, inside_humidity, label= "Humidor Humidity")
plt.plot(id, outside_humidity, label= "Outside Humdidty")
plt.legend()
plt.axhspan(60, 75, color='green', alpha=0.3)
plt.axhspan(40, 60, color="red", alpha=0.1)

# Add titles to the chart and axes
plt.title("Humidor Historical Humidity", fontsize=20)
plt.ylabel("Humidity Level", fontsize=20)
plt.xlabel("ID", fontsize=20)

# Place the "green range" of the plot
plt.savefig('~/flask/static/images/humidor_graph.png')