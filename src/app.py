import time
import RPi.GPIO as GPIO
import monitor as batMonitor

from adxl345 import ADXL345
from device_status import DeviceStatus

# Total motion duration for suspicious motion (seconds)
watch_total_duration = 3

#Interrupt watch interval duration (seconds)
watch_interval = 1

# Consecutive number of interrupts to determine suspicious motion
trig_int_threshold = watch_total_duration / watch_interval
trig_int_count = 0

# Set GPIO mode to use board numbering scheme
GPIO.setmode(GPIO.BOARD)

# GPIO pins
INT1 = 13
INT2 = 15
alarm = 16

# Set GPIO pin directions
GPIO.setup([INT1, INT2], GPIO.IN)
GPIO.setup(alarm, GPIO.OUT)

# Create device status object
device_status = DeviceStatus()

# Setup ADXL345 and enable measurement mode
adxl345 = ADXL345()
adxl345.run()

#take a measurement every minute
poll_interval = 5
time_counter = 0
GPIO.output(alarm,1)

while True:
    # Wait for interrupt interval
    
    #if (time_counter >= poll_interval):
     #   battery = batMonitor.bmonitor();
      #  print(battery)
       # time_counter = 0;
    #else:
     #   time_counter += 1
  
    time.sleep(watch_interval)
    print('Time = {}'.format(time_counter))
    
    print('Interrupt count = {}'.format(trig_int_count))
    
    if (GPIO.input(INT1)):
        trig_int_count += 1
        adxl345.clear_int()
    else:
        trig_int_count = 0
    
    if (trig_int_count >= trig_int_threshold):
        GPIO.output(alarm, 0)
        print(GPIO.input(alarm))
        print('TAMPERING DETECTED')
        # delete after... just to shut off the alarm now. 
        time.sleep(5)
        GPIO.output(alarm, 1)
        trig_int_count = 0

