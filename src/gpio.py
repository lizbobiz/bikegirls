import RPi.GPIO as GPIO


# GPIO pins
INT1 = 13
ALARM = 16


def init_gpio():
    # Set GPIO mode to use board numbering scheme
    GPIO.setmode(GPIO.BOARD)
    
    # Set GPIO pin directions
    GPIO.setup(INT1, GPIO.IN)
    GPIO.setup(ALARM, GPIO.OUT)
