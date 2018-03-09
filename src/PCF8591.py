import smbus


# Maybe this should change ?
bus = smbus.SMBus(1)

# This is the address we setup in the PCF8591
address = 0x48
class PCF8591:
	

# 0x00 - 0x03 is AIN0 - AIN3
# bus.write_byte(address,0x00)

# I think we only need one channel

		def read_channel(ch):
			try:
			if ch == 0: 
				bus.write_byte(address, 0x40)
				bus.read_byte(address) # It needs a dummy read to start conversion
			if ch == 1:
				bus.write_byte(address, 0x41)
				bus.read_byte(address)
			if ch == 2: 
				bus.write_byte(address, 0x42)
				bus.read_byte(address)
			if ch == 3: 
				bus.write_byte(address, 0x43)
				bus.read_byte(address)
			bus.read_byte(address)
			return bus.read_byte(address)
			
		def write(val)
			try:
				temp = val
				temp = int(temp)
				bus.write_byte_data(address, 0x40, temp)
           
       
		
