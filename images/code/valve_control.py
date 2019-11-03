#!/usr/bin/python3
##------------------------------------------
##--- Author: Chip Fleming
##--- Date: 22 September 2019
##--- Version: 1.0
##--- Python Ver: 3.7
##------------------------------------------

#import system to allow the use of command line arguments
import sys

#import time class to allow use of sleep method
import time

#import the GPIO DigitalOutputDevice class to handle the valve enable function
from gpiozero import DigitalOutputDevice

#import the GPIO Motor class to handle the valve direction
from gpiozero import Motor

#import the class definition from "email_handler.py" file
from email_handler import Class_eMail


#valve_closed = DigitalInputDevice(14, pull_up=True, bounce_time=1)
#valve_open = DigitalInputDevice(15, pull_up=True, bounce_time=1)

def send_valve_commanded_close():
    email = Class_eMail()
    email.send_Text_Mail('', "The drip irrigation system master water valve is being commanded to close.")
    del email 

def send_valve_commanded_open():
    email = Class_eMail()
    email.send_Text_Mail('', "The drip irrigation system master water valve is being commanded to open.")
    del email
    
def send_valve_commanded_stop():
    email = Class_eMail()
    email.send_Text_Mail('', "The drip irrigation system master water valve is being commanded to stop.")
    del email
    
def send_valve_command_error():
    email = Class_eMail()
    email.send_Text_Mail('', "The drip irrigation system master water valve control function was called with an invalid argument.")
    del email

# Get the command line action argument (open or close)
command = str(sys.argv[1])

valve = Motor(5, 6, 13)

if command in ['close', 'CLOSE']:
    valve.backward()    
    send_valve_commanded_close()
    
    time.sleep(10)
    
    valve.stop()    
    send_valve_commanded_stop()


elif command in ['open', 'OPEN']:
    valve.forward()    
    send_valve_commanded_open()
    
    time.sleep(10)
    
    valve.stop()    
    send_valve_commanded_stop()

    
else:
    valve.stop()
    send_valve_command_error()
