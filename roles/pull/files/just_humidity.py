#!/usr/bin/env python3
import board
import adafruit_bme680

def how_humid():
    i2c = board.I2C()
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    inside_humidity = format(bme680.relative_humidity, '.1f')
    return(inside_humidity)

if __name__ == '__main__':
    how_humid()