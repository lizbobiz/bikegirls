# Standard library imports
import logging

# Third-party imports
import RPi.GPIO as GPIO

# Local imports
import gpio
from adxl345 import ADXL345


class MotionWatch:
    def __init__(self):
        # Total watch duration (seconds)
        self.watch_duration = 3
        # Interrupt watch interval (interrupts/second)
        self.watch_interval = 1
        # Consecutive interrupt threshold for suspicious motion (interrupts)
        self.trig_int_threshold = self.watch_duration*self.watch_interval
        # Consecutive interrupt counter (interrupts)
        self.trig_int_count = 0
        
        # Setup ADXL345
        self.adxl345 = ADXL345()
    
    def enable(self):
        self.adxl345.run()
    
    def disable(self):
        self.adxl345.standby()
    
    def is_motion_detected(self):
        # If interrupt was generated, clear it and increment interrupt count
        if (GPIO.input(gpio.INT1)):
            logging.debug('Interrupt count incremented to %s' % (self.trig_int_count))
            self.trig_int_count += 1
            self.adxl345.clear_int()
        # If no interrupt was generated, reset interrupt count
        else:
            logging.debug('Interrupt count reset to 0')
            self.trig_int_count = 0
        
        # If count is above threshold, return true and reset count
        if self.trig_int_count >= self.trig_int_threshold:
            logging.debug('Suspicious motion detected')
            self.trig_int_count = 0
            return True
        # If count is below threshold, return false
        else:
            return False
    
    def trigger_alarm(self):
        GPIO.output(gpio.ALARM, 1)
    
    def disarm_alarm(self):
        GPIO.output(gpio.ALARM, 0)
