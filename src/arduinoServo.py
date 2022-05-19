#!/usr/bin/env python3
#"""Control an Arduino over the USB port."""
# usb.py
# Created by John Woolsey on 12/17/2019.
# Copyright (c) 2019 Woolsey Workshop.  All rights reserved.
#USB_PORT = "2341:0001"  # Arduino Uno R3 Compatible
#USB_PORT = "/dev/ttyACM1"  # Arduino Uno WiFi Rev2
# Imports# servo control 15.12.2016
 
# 1) user set servo position in python
# 2) position is sent to arduino
# 3) arduino moves servo to position
# 4) arduino send confirmation message back to python
# 5) message is printed in python console
 

import serial
import time
import warnings
import serial.tools.list_ports

arduino_ports = None
arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description  # may need tweaking to match new arduinos
    ]

if not arduino_ports:
    #raise IOError("No Arduino found")
    print("No Arduino")

if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

#ser = serial.Serial(arduino_ports[0])


print(arduino_ports)
#print(ser.port)



arduino = serial.Serial(port=arduino_ports[0], baudrate=115200, timeout=.2)


#print("No arduino")

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
    
def lookUp ():
    write_readx(str(5))
    
def lookDown ():
    write_readx(str(6))
    
def notNod():
    write_readx(str(7))

def ledSpeaking():
    write_readx(str(11))

def ledListening():
    write_readx(str(12))
    
def ledOff():
    write_readx(str(13))

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
    
    
    
    

    
    