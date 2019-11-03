#!/usr/bin/python3
'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: http://randomnerdtutorials.com
Modified by Chip Fleming 23Sep2019 for valve control

'''
import time
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
from email_handler import Class_eMail

app = Flask(__name__)

def send_valve_close():
    """Send command valve to close message."""
    email = Class_eMail()
    email.send_Text_Mail('', "The drip irrigation system master water valve is being commanded to close.")
    del email
 
def send_valve_open():
    """Send command valve to open message."""
    email = Class_eMail()
    email.send_Text_Mail('', "The drip irrigation system master water valve is being commanded to open.")
    del email

def send_valve_stop():
    """Send command valve to stop message."""
    email = Class_eMail()
    email.send_Text_Mail('', "The drip irrigation system master water valve is being commanded to stop.")
    del email

def send_error_message(error_message):
    """Send error message upon invocation with invalid argument."""
    email = Class_eMail()
    email.send_Text_Mail('', error_message)
    del email

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    5  : {'name' : 'GPIO 5', 'state' : GPIO.LOW},
    6  : {'name' : 'GPIO 6', 'state' : GPIO.LOW},
    13 : {'name' : 'GPIO 13', 'state' : GPIO.LOW},
    14 : {'name' : 'GPIO 14', 'state' : GPIO.LOW},
    15 : {'name' : 'GPIO 15', 'state' : GPIO.LOW}
    }

# Set each pin as an output and make it low:
for pin in pins:
    if pin == 14:
        break
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

@app.route("/")
def main():
    """Provide the initial/default web page response."""
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins' : pins
    }
    # Pass the template data into the template boot_starter.html and return it to the user
    return render_template('boot_starter.html', **templateData)

# The function below is executed when someone requests a URL with the valve action in it:
@app.route("/changeValve/<action>")
def takeAction(action):
    """Take action based on the arguments provided in the GET."""
    # If the action part of the URL is "open," execute the code indented below:
    if action == "open":
        # Set IN1 (pin 5) high and IN2 (pin 6) low
        send_valve_open()

        GPIO.output(13, GPIO.HIGH)
        GPIO.output(5, GPIO.HIGH)
        GPIO.output(6, GPIO.LOW)
        
        time.sleep(10)
        
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        
        #send_valve_stop
        

    if action == "close":
        send_valve_close()

        GPIO.output(13, GPIO.HIGH)
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        time.sleep(10)
        
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        
        #send_valve_stop

    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'pins' : pins
    }

    return render_template('boot_starter.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090, debug=False)
