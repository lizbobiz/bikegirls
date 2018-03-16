# Standard library imports
import logging
import sys
import threading
import time

# Third-party imports
from firebase_admin import db

# Local imports
import gpio
from device_status import DeviceStatus
from motion_watch import MotionWatch
from server import get_fcm_app, delete_fcm_app, Client
from monitor import bmonitor, low_battery_shutdown, voltage_divider

#battery_counter = 0
# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)7s %(module)12s:%(lineno)-4s %(message)s')
    
#battery_counter = 0
device_status = DeviceStatus()
fcm_app = get_fcm_app()
db.reference('device_status').set(vars(device_status))

sys.exit()

def main_thread():
    # Configuation GPIO pins
    gpio.init_gpio()

    #battery=bmonitor()
   

    # Create Firebase app instance
    fcm_app = get_fcm_app()

    # Create and initialize XMPP client instance
    
    client = Client()
    
    # Create device status object and push it up to database
    device_status = DeviceStatus()
    db.reference('device_status').set(vars(device_status))

    # Create motion watch object
    motion_watch = MotionWatch()
        
    # Main program loop
    while True:
        logging.debug('New main loop iteration')
        
        # If device is enabled, check for motion
        if device_status.armed:
            logging.debug('Checking for suspicious motion')
            if motion_watch.is_motion_detected():
                logging.debug('Suspicious motion detected')
                
                # Trigger alarm
                motion_watch.trigger_alarm()
                logging.debug('Alarm triggered')
                
                # Send push notification if not already sent
                if not device_status.triggered:
                    client.send_notification('Your Bike', 'Hey, it\'s me, your bike. I am being stolen. Pls halp.')
                
                # Update device status
                device_status.triggered = True
                
                logging.debug('Push notification sent')
        
        # Update battery percentage
        
        # Check for requests from app
        
        if client.cmd_q:
            cmd = client.cmd_q.pop(0)
            logging.debug('%s command popped from queue' % (cmd))
            
            if cmd == 'TOGGLE_ARMED':
                device_status.armed = not device_status.armed
                if device_status.armed:
                    motion_watch.enable()
                else:
                    motion_watch.disable()
                logging.debug('Device status armed toggled')
            elif cmd == 'DISARM_ALARM':
                device_status.triggered = False
                motion_watch.disarm_alarm()
                logging.debug('Alarm disarmed and device status updated')
        
        # Push device stastus object up to database
        print '\n\nFLAG1\n\n'
        ref = db.reference('device_status')
        print '\n\nFLAG2\n\n'
        ref.set(vars(device_status))
        logging.debug('Device status pushed to database')
        
        # Sleep for watch interval duration
        time.sleep(motion_watch.watch_interval)

    # Disconnect XMPP client
    client.disconnect()

    # Delete Firebase app instance
    delete_fcm_app(fcm_app)

thread = threading.Thread(target=main_thread)
thread.start()
