import time

#from valve_sim import valve_closed
#from valve_sim import valve_open

#import the GPIO class to handle the valve state
from gpiozero import DigitalInputDevice

#import logging
import sys

class State_Machine:
    #logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    
    valve_closed = DigitalInputDevice(15, pull_up=True, bounce_time=1)
    valve_open = DigitalInputDevice(14, pull_up=True, bounce_time=1)

    DEBOUNCE_TIME = 0.5

    def __init__(self, closed_state=0, open_state = 0, 
                 closed_active_start_time = 0, closed_inactive_start_time = 0, closed_inactive_time = 0,
                 open_active_start_time = 0, open_inactive_start_time = 0, open_inactive_time = 0):
        self.closed_state = -1
        self.open_state = -1
        self.closed_active_start_time = 0.0
        self.closed_inactive_start_time = 0.0
        self.closed_inactive_time = 0.0
        self.open_active_start_time = 0.0
        self.open_inactive_start_time = 0.0
        self.open_inactive_time = 0.0
        
    def __str__(self):
        return "self.closed_state = {}, self.open_state = {}".format(self.closed_state, self.open_state)
    
    def closed_state_zero(self):   #closed has been detected active once
        if self.valve_closed.value == 1:
            self.closed_active_start_time = time.monotonic()
            #logging.debug('Closed State 0 going to 1')
            self.closed_state = 1
        else:
            #logging.debug('Closed State 0 going to 3')
            self.closed_state = 3
            
        return self.closed_state

    def closed_state_one(self):    #waiting for close to be detected active for > debounce time
        if time.monotonic() - self.closed_active_start_time > self.DEBOUNCE_TIME:
            if self.valve_closed.value == 1:
                #logging.debug('Closed State 1 going to 2')
                self.closed_state = 2
            else:
                #logging.debug('Closed State 1 going to 3')
                self.closed_state = 3
                
        return self.closed_state            

    def closed_state_two(self):    #closed has been detected active for > debounce time 
        if self.valve_closed.value == 0:
            #logging.debug('Closed State 2 going to 3')
            self.closed_state = 3
            
        return self.closed_state
        
    def closed_state_three(self):  #closed has been detected inactive once
        if self.valve_closed.value == 0:
            self.closed_inactive_start_time = time.monotonic()
            #logging.debug('Closed State 3 going to 4')
            self.closed_state = 4
        else:
            #logging.debug('Closed State 3 going to 0')
            self.closed_state = 0
            
        return self.closed_state

    def closed_state_four(self):   #waiting for close to be detected inactive for > debounce time
        if time.monotonic() - self.closed_inactive_start_time > self.DEBOUNCE_TIME:
            if self.valve_closed.value == 0:
                #logging.debug('Closed State 4 going to 5')
                self.closed_state = 5
            else:
                #logging.debug('Closed State 4 going to 0')
                self.closed_state = 0 

        return self.closed_state            
            
    def closed_state_five(self):   #closed has been detected inactive for > debounce time
        self.closed_inactive_time = time.monotonic() - self.closed_inactive_start_time
        if self.valve_closed.value == 1:
            #logging.debug('Closed State 5 going to 0')
            self.closed_inactive_time = 0
            self.closed_state = 0
            
        return self.closed_state

    def closed_state_update(self, closed_state):
        closed_switcher = {
            0: self.closed_state_zero,
            1: self.closed_state_one,
            2: self.closed_state_two,
            3: self.closed_state_three,
            4: self.closed_state_four,
            5: self.closed_state_five
        }
        if self.closed_state < 0 or self.closed_state > 5:
            closed_func = self.closed_state_zero
        else:
            closed_func = closed_switcher[self.closed_state]
        #logging.debug(closed_func)
        self.closed_state = closed_func()

    def open_state_zero(self):   #open has been detected active once
        if self.valve_open.value == 1:
            self.open_active_start_time = time.monotonic()
            self.open_state = 1
        else:
            self.open_state = 3

        return self.open_state

    def open_state_one(self):    #waiting for open to be detected active for > debounce time
        if time.monotonic() - self.open_active_start_time > self.DEBOUNCE_TIME:
            if self.valve_open.value == 1:
                self.open_state = 2
            else:
                self.open_state = 3

        return self.open_state

    def open_state_two(self):    #open has been detected active for > debounce time 
        if self.valve_open.value == 0:
            self.open_state = 3

        return self.open_state

    def open_state_three(self):  #open has been detected inactive once
        if self.valve_open.value == 0:
            self.open_inactive_start_time = time.monotonic()
            self.open_state = 4
        else:
            self.open_state = 0

        return self.open_state

    def open_state_four(self):   #waiting for open to be detected inactive for > debounce time
        if time.monotonic() - self.open_inactive_start_time > self.DEBOUNCE_TIME:
            if self.valve_open.value == 0:
                self.open_state = 5
            else:
                self.open_state = 0

        return self.open_state

    def open_state_five(self):   #open has been detected inactive for > debounce time
        self.open_inactive_time = time.monotonic() - self.open_inactive_start_time
        if self.valve_open.value == 1:
            self.open_inactive_time = 0
            self.open_state = 0

        return self.open_state

    def open_state_update(self, open_state):
        open_switcher = {
            0: self.open_state_zero,
            1: self.open_state_one,
            2: self.open_state_two,
            3: self.open_state_three,
            4: self.open_state_four,
            5: self.open_state_five
        }
        if self.open_state < 0 or self.open_state > 5:
            open_func = self.open_state_zero
        else:
            open_func = open_switcher[self.open_state]
        #logging.debug(open_func)
        self.open_state = open_func()


