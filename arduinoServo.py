#!/usr/bin/env python3
#"""Control an Arduino over the USB port."""
# usb.py
# Created by John Woolsey on 12/17/2019.
# Copyright (c) 2019 Woolsey Workshop.  All rights reserved.
#USB_PORT = "2341:0001"  # Arduino Uno R3 Compatible
USB_PORT = "/dev/ttyACM1"  # Arduino Uno WiFi Rev2
# Imports# servo control 15.12.2016
 
# 1) user set servo position in python
# 2) position is sent to arduino
# 3) arduino moves servo to position
# 4) arduino send confirmation message back to python
# 5) message is printed in python console
 

import serial
import time

arduino = serial.Serial(port=USB_PORT, baudrate=115200, timeout=.1)


def write_readx(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def lookLeft ():
    write_readx(str(2))
    
def lookRight ():
    write_readx(str(3))
    
def nod ():
    write_readx(str(1))
    
def lookStraight ():
    write_readx(str(4))

#while True:
#    lookLeft()
#    time.sleep(0.5)
#    lookRight()
#    time.sleep(0.5)
    #num = input("Enter a number1: ")
    #value = write_readx(num)
    #print(value)       # print arduino echo to console
    
    # nod = 1
    #look left = 2
    #look right = 3
    #look straight = 4
    
    
    
    

    
    