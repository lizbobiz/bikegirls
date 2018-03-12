import smbus


# Maybe this should change ?
bus = smbus.SMBus(1)

# This is the address we setup in the PCF8591
address = 0x48

	

# 0x00 - 0x03 is AIN0 - AIN3
# bus.write_byte(address,0x00)

# I think we only need one channel

def read_channel(ch):
    try:
        if ch == 0: 
            bus.write_byte(address, 0x40)
        if ch == 1:
            bus.write_byte(address, 0x41)
        if ch == 2: 
            bus.write_byte(address, 0x42)
        if ch == 3: 
            bus.write_byte(address, 0x43)
        bus.read_byte(address)
    except Exception, e:
        print "Address: %s" % address
        print e
    return bus.read_byte(address)


           
   
		
