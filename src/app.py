import time
import RPi.GPIO as GPIO
import monitor as batMonitor

from adxl345 import ADXL345
from device_status import DeviceStatus

# Total motion duration for suspicious motion (seconds)
watch_total_duration = 3

# Interrupt watch interval duration (seconds)
watch_interval = 1

# Consecutive number of interrupts to determine suspicious motion
trig_int_threshold = watch_total_duration / watch_interval
trig_int_count = 0

# Set GPIO mode to use board numbering scheme
GPIO.setmode(GPIO.BOARD)

# GPIO pins
INT1 = 13
INT2 = 15
Alarm = 12

# Set GPIO pin directions
GPIO.setup([INT1, INT2], GPIO.IN)
GPIO.setup(alarm, GPIO.OUT)

# Create device status object
device_status = DeviceStatus()

# Setup ADXL345 and enable measurement mode
adxl345 = ADXL345()
adxl345.run()

while True:
    # Wait for interrupt interval
    battery = batMonitor.battery_monitor();
    print(battery)
  
    time.sleep(watch_interval)
    
    print('Interrupt count = {}'.format(trig_int_count))
    
    if (GPIO.input(INT1)):
        trig_int_count += 1
        adxl345.clear_int()
    else:
        trig_int_count = 0
    
    if (trig_int_count >= trig_int_threshold):
        GPIO.output(alarm, 1)
        print('TAMPERING DETECTED')
        # delete after... just to shut off the alarm now. 
        sleep(0.5)
        GPIO.output(alarm, 0)
        trig_int_count = 0

