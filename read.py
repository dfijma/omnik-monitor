#!/usr/bin/python3 -u
import urllib.request
from datetime import datetime

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.MCP230xx as MCP
import time
import math
import smbus
import sys

# get i2c bus
bus = smbus.SMBus(1)

# Define MCP pins connected to the LCD.
lcd_rs        = 1
lcd_en        = 2
lcd_d4        = 3
lcd_d5        = 4
lcd_d6        = 5
lcd_d7        = 6
lcd_back      = 7

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# get lcd via gpio extender
gpio = MCP.MCP23008(0x20, busnum=1)
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_back,
                           gpio=gpio, invert_polarity=False)


# yuck, but works: https://github.com/Woutrrr/Omnik-Data-Logger/issues/27
url="http://192.168.179.30/js/status.js"
#url="http://10.10.100.254/js/status.js"

def read():
  try:
    for line in urllib.request.urlopen(url):
       d = line.decode('ascii',errors="ignore")
       if "myDeviceArray[0]=" in d:
           # print(d.split(','))
           ps=d.split(',')
           [now,today,total]=ps[5:8]
           now=int(now) # in W
           today=int(today) # 1/100's of kWh
           total=int(total)*10 # convert 1/10's to 1/100; of kWh
           msg="%d %.2f %.2f" % (now, today/100, total/100)
           print(msg)
           line1="%s %4dW     " % (datetime.now().strftime("%H:%M"), now)
           line2="%.1fkWh %.1fkWh " % (today / 100, total / 100)
           lcd.set_cursor(0,0)
           lcd.message(line1)
           lcd.set_cursor(0,1)
           lcd.message(line2)
           break
  except Exception as inst:
    print("error: ", inst)

while True:
    read()
    time.sleep(2)
