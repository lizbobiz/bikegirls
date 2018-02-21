import os
import smbus

# Get bus for I2C
bus_number = int(os.getenv('I2C_BUS'))
bus = smbus.SMBus(bus_number)

# Register addresses
POWER_CTL = 0x2D        # Power-saving features control     (r/w)

INT_ENABLE = 0x2E       # Interrupt enable control          (r/w)
INT_MAP = 0x2F          # Interrupt mapping control         (r/w)
INT_SOURCE = 0x30       # Source of interrupts              (r)

FIFO_CTL = 0x38         # FIFO control                      (r/w)
FIFO_STATUS = 0x39      # FIFO status                       (r)

DATAX0 = 0x32           # x-axis data 0                     (r)
DATAX1 = 0x33           # x-axis data 1                     (r)
DATAY0 = 0x34           # y-axis data 0                     (r)
DATAY1 = 0x35           # y-axis data 1                     (r)
DATAZ0 = 0x36           # z-axis data 0                     (r)
DATAZ1 = 0x37           # z-axis data 1                     (r)

THRESH_TAP = 0x1D       # Tap threshold                     (r/w)
DUR = 0x21              # Tap duration                      (r/w)

# Register values
MEASURE = 0x08          # [D3] = 1'b1 in POWER_CTL

SINGLE_TAP = 0x40       # [D6] = 1'b1 in INT_ENABLE

FIFO_MODE = 0x40        # [D7:D6] = 2'b10 in FIFO_CTL
TRIGGER = 0x20          # [D5] = 1'b0 in FIFO_CTL
SAMPLES = 0x01          # [D4:D0] = 5'b00001 in FIFO_CTL

THRESHOLD = 0x08        # [D7:D0] = 8'd8 in THRESH_TAP
DURATION = 0x04         # [D7:D0] = 8'd4 in DUR


class ADXL345:
    addr = None

    def __init__(self, addr=0x53):
        self.addr = addr
        self.config_tap()
        self.config_fifo()
        self.config_int()

    def config_tap(self):
        # Configure tap interrupts for specified threshold and duration
        bus.write_byte_data(self.addr, THRESH_TAP, THRESHOLD)
        bus.write_byte_data(self.addr, DUR, DURATION)

    def config_fifo(self):
        # Configure FIFO for FIFO mode with interrupts on INT1 triggered by one FIFO entry
        bus.write_byte_data(self.addr, FIFO_CTL, FIFO_MODE | TRIGGER | SAMPLES)

    def config_int(self):
        # Enable interrupts triggered by SINGLE_TAP
        bus.write_byte_data(self.addr, INT_ENABLE, SINGLE_TAP)

    def run(self):
        # Enable measurement mode
        bus.write_byte_data(self.addr, POWER_CTL, MEASURE)

    def clear_int(self):
        # Read from all six axis data registers
        bus.read_i2c_block_data(self.addr, DATAX0, 6)
