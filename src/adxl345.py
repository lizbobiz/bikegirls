import os
import smbus

# Get bus for I2C
bus = smbus.SMBus(1)

########################################################################

# Register addresses
POWER_CTL = 0x2D        # Power-saving features control     (r/w)

INT_ENABLE = 0x2E       # Interrupt enable control          (r/w)
INT_MAP = 0x2F          # Interrupt mapping control         (r/w)
INT_SOURCE = 0x30       # Source of interrupts              (r)

FIFO_CTL = 0x38         # FIFO control                      (r/w)
FIFO_STATUS = 0x39      # FIFO status                       (r)

THRESH_ACT = 0x24       # Activity threshold                (r/w)
ACT_INACT_CTL = 0x27    # Axis enable for activity int      (r/w)

########################################################################

# Register values
MEASURE = 0x08          # [D3] = 1'b1 in POWER_CTL

ACTIVITY = 0x10         # [D4] = 1'b1 in INT_ENABLE/INT_MAP

FIFO_MODE = 0x80        # [D7:D6] = 2'b10 in FIFO_CTL

ACT_THRESHOLD = 0x20    # [D7:D0] = 8'd8 in THRESH_ACT
ACT_CONFIG = 0x70       # [D7:D0] = 8'h70 in ACT_INACT_CTL

########################################################################

class ADXL345:
    addr = None

    def __init__(self, addr=0x53):
        self.addr = addr
        self.config_act()
        self.config_fifo()
        self.config_int()

    def config_act(self):
        # Configure activity interrupts for specified threshold and axes
        bus.write_byte_data(self.addr, THRESH_ACT, ACT_THRESHOLD)
        bus.write_byte_data(self.addr, ACT_INACT_CTL, ACT_CONFIG)

    def config_fifo(self):
        # Configure FIFO for stream mode
        bus.write_byte_data(self.addr, FIFO_CTL, FIFO_MODE)

    def config_int(self):
        # Enable interrupts triggered by ACTIVITY and send them to INT1
        bus.write_byte_data(self.addr, INT_MAP, 0x00)
        bus.write_byte_data(self.addr, INT_ENABLE, ACTIVITY)

    def run(self):
        # Enable measurement mode
        bus.write_byte_data(self.addr, POWER_CTL, MEASURE)
    
    def standby(self):
        # Enable standby mode
        bus.write_byte_data(self.addr, POWER_CTL, 0x00)

    def clear_int(self):
        # Read INT_SOURCE register to clear interrupts
        bus.read_byte_data(self.addr, INT_SOURCE)
