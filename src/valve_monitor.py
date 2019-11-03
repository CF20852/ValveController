#!/usr/bin/python3
##------------------------------------------
##--- Author: Chip Fleming
##--- Date: 15 September 2019
##--- Version: 1.0
##--- Python Ver: 3.7
##------------------------------------------

#import the GPIO class to handle the valve state
#from gpiozero import DigitalInputDevice

#import the class definition from "email_handler.py" file
from email_handler import Class_eMail

#import the open/close debounce state machine
from state_machines import State_Machine

sm = State_Machine()

#valve_closed = DigitalInputDevice(15, pull_up=True, bounce_time=1)
#valve_open = DigitalInputDevice(14, pull_up=True, bounce_time=1)

# Send valve closed message 
def send_valve_closed():
    email = Class_eMail()
    email.send_Text_Mail('', "The drip irrigation system master water valve is closed.")
    print("The drip irrigation system master water valve is closed.", flush=True)
    del email
    return

# Send valve open message 
def send_valve_open():
    email = Class_eMail()
    email.send_Text_Mail('', "The drip irrigation system master water valve is open.")
    print("The drip irrigation system master water valve is open.", flush=True)
    del email
    return

# Send valve stuck message
def send_valve_stuck():
    email = Class_eMail()
    email.send_Text_Mail('', "The drip irrigation system master water valve is in an indeterminate state.")
    print("The drip irrigation system master water valve is in an indeterminate state.", flush=True)
    del email
    return
    
 
valve_closed_sent = False
valve_open_sent = False
valve_stuck_sent = False

while True:
    sm.closed_state_update(sm.closed_state)
    sm.open_state_update(sm.open_state)
    
    if sm.closed_state == 2 and valve_closed_sent == False:
        send_valve_closed()
        valve_closed_sent = True
        valve_open_sent = False        
        valve_stuck_sent = False
        
    if sm.open_state == 2 and valve_open_sent == False:
        send_valve_open()
        valve_open_sent = True
        valve_closed_sent = False
        valve_stuck_sent = False
        
    if sm.closed_inactive_time > 15 and sm.open_inactive_time > 15 and valve_stuck_sent == False:
        send_valve_stuck()
        valve_stuck_sent = True
        valve_closed_sent = False
        valve_open_sent = False
        
       
