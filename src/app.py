import time
import RPi.GPIO as GPIO

from src.adxl345 import ADXL345
from src.device_status import DeviceStatus

# Set GPIO mode to use board numbering scheme
GPIO.setmode(GPIO.BOARD)

# GPIO pins
INT1 = 11
INT2 = 13

# Set GPIO pin directions
GPIO.setup([INT1, INT2], GPIO.IN)

# Create device status object
device_status = DeviceStatus()

# Setup ADXL345 and enable measurement mode
adxl345 = ADXL345()
adxl345.run()

"""
while True:
    # Poll interrupt signal
    if GPIO.input(INT1):
        # Update device status (triggered)
        DeviceStatus.triggered = True
        # Trigger alarm signal

        # Clear interrupt
        adxl345.clear_int()

    # Poll data from app

    # Update device status (battery)

    time.sleep(0.5)
"""

while True:
    if GPIO.input(INT1):
        print('INT1 is high')
        adxl345.clear_int()
    time.sleep(0.5)
