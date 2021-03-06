import PCF8591 as ADC
import logging
import time
import os
import RPi.GPIO as GPIO


# LiPo battery voltage range - 
###### Change these values as well

batt_min_voltage = 6.8
batt_max_voltage = 7.4



# Define the minimum battery level at which shutdown is triggered

fraction_battery_min = 0.075

safe_mode = True
# Voltage divider drops the battery voltage from around 7V to under 3.3V which is the limit for the Pi
##### These values are not correct
vd_r1 = 509.2
vd_r2 = 387.3

gpio_min_voltage = 0.0
gpio_max_voltage = 3.3

## if we are using channel 0
v_bat_adc_pin = 2;

def voltage_divider(r1, r2, vin):
    vout = vin * (r2 / (r1 + r2))
    return vout
    
def low_battery_shutdown():
    global safe_mode

    shutdown_delay = 30 # seconds

    # in Safe Mode, wait 2 mins before actually shutting down
    if(safe_mode):
        cmd = "sudo wall 'System shutting down in 2 minutes - SAFE MODE'"
        os.system(cmd)
        time.sleep(120)

    cmd = "sudo wall 'System shutting down in %d seconds'" % shutdown_delay
    os.system(cmd)
    time.sleep(shutdown_delay)
    # Log message is added to /var/log/messages
    os.system("sudo logger -t 'pi_power' '** Low Battery - shutting down now **'")
    GPIO.cleanup()
    os.system("sudo shutdown now")

def bmonitor():
    # this is the effective max voltage, prior to the divider, that the ADC can register
    v_out = voltage_divider(vd_r1,vd_r2, batt_max_voltage)
    
    adc_conversion_factor = (gpio_max_voltage /v_out)*batt_max_voltage
    logging.debug('adc_conversion_factor = %f' % adc_conversion_factor)
    
    # read the analog pins on the ACD (range 0-256) and convert to 0.0-1.|0
    frac_v_bat = round(ADC.read_channel(v_bat_adc_pin)) / 255.0
    logging.debug('frac_v_bat = %f' % frac_v_bat)
    
    v_bat = frac_v_bat*adc_conversion_factor
    logging.debug('v_bat = %f' % v_bat)
    
    fraction_battery = (v_bat - batt_min_voltage)/(batt_max_voltage - batt_min_voltage)
    logging.debug('fraction_battery = %f' % fraction_battery)
    
    if fraction_battery < fraction_battery_min:
        print "** LOW BATTERY - shutting down........"
        low_battery_shutdown()
    
    if fraction_battery > 1.0:
        fraction_battery = 1.0
    
    ## return the value of the battery fraction
    return fraction_battery
