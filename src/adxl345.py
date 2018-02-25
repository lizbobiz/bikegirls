import os
import smbus

# Get bus for I2C
bus = smbus.SMBus(1)

# Register addresses
POWER_CTL = 0x2D        # Power-saving features control     (r/w)

INT_ENABLE = 0x2E       # Interrupt enable control          (r/w)
INT_MAP = 0x2F          # Interrupt mapping control         (r/w)
INT_SOURCE = 0x30       # Source of interrupts              (r)

FIFO_CTL = 0x38         # FIFO control                      (r/w)
FIFO_STATUS = 0x39      # FIFO status                       (r)

THRESH_ACT = 0x24       # Activity threshold                (r/w)
THRESH_INACT = 0x25     # Inactivity threshold              (r/w)
TIME_INACT = 0x26       # Inactivity time                   (r/w)
ACT_INACT_CTL = 0x27    # Axis enable for activity int      (r/w)

DATAX0 = 0x32           # x-axis data 0                     (r)
DATAX1 = 0x33           # x-axis data 1                     (r)
DATAY0 = 0x34           # y-axis data 0                     (r)
DATAY1 = 0x35           # y-axis data 1                     (r)
DATAZ0 = 0x36           # z-axis data 0                     (r)
DATAZ1 = 0x37           # z-axis data 1                     (r)

# Register values
MEASURE = 0x08          # [D3] = 1'b1 in POWER_CTL

ACTIVITY = 0x10         # [D4] = 1'b1 in INT_ENABLE/INT_MAP
INACTIVITY = 0x08       # [D3] = 1'b1 in INT_ENABLE/INT_MAP

FIFO_MODE = 0x80        # [D7:D6] = 2'b10 in FIFO_CTL
TRIGGER = 0x00          # [D5] = 1'b0 in FIFO_CTL
SAMPLES = 0x00          # [D4:D0] = 5'b00001 in FIFO_CTL

ACT_THRESHOLD = 0x20    # [D7:D0] = 8'd8 in THRESH_ACT
INACT_THRESHOLD = 0x20  # [D7:D0] = 8'd8 in THRESH_INACT
INACT_TIME = 0x05       # [D7:D0] = 8'd5 in INACT_TIME
ACT_CONFIG = 0x77       # [D7:D0] = 8'h77 in ACT_INACT_CTL


class ADXL345:
    addr = None

    def __init__(self, addr=0x53):
        self.addr = addr
        self.config_act_inact()
        self.config_fifo()
        self.config_int()

    def config_act_inact(self):
        # Configure activity interrupts for specified threshold and axes
        bus.write_byte_data(self.addr, THRESH_ACT, ACT_THRESHOLD)
        bus.write_byte_data(self.addr, THRESH_INACT, INACT_THRESHOLD)
        bus.write_byte_data(self.addr, TIME_INACT, INACT_TIME)
        bus.write_byte_data(self.addr, ACT_INACT_CTL, ACT_CONFIG)

    def config_fifo(self):
        # Configure FIFO for FIFO mode with interrupts on INT1 triggered by one FIFO entry
        bus.write_byte_data(self.addr, FIFO_CTL, FIFO_MODE | TRIGGER | SAMPLES)

    def config_int(self):
        # Enable interrupts triggered by ACTIVITY and send them to INT1
        bus.write_byte_data(self.addr, INT_MAP, ACTIVITY | INACTIVITY)
        bus.write_byte_data(self.addr, INT_ENABLE, ACTIVITY | INACTIVITY)

    def run(self):
        # Enable measurement mode
        bus.write_byte_data(self.addr, POWER_CTL, MEASURE)

    def clear_int(self):
        # Read from all six axis data registers
        bus.read_byte_data(self.addr, INT_SOURCE)
        print('Interrupt cleared')

