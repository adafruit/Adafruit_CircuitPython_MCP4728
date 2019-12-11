import time
import board
import busio
import adafruit_mcp4728

i2c = busio.I2C(board.SCL, board.SDA)
mcp4728 =  adafruit_mcp4728.MCP4728(i2c)

def print_regs():
    buf = bytearray(24)

    with mcp4728.i2c_device as i2c:
        i2c.readinto(buf)

    for index, value in enumerate(buf):
        if index %3 is 0:
            print("\n%4s\t"%index, end="")
        print("%s %s "%( format(value, '#010b'), hex(value)), end="")
    print()

# Create a function called "chunks" with two arguments, l and n:
def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]
# Create a list that from the results of the function chunks:

# mcp4728._channel_a_multi_write = 0b0000111111111111 # Voltage = VCC
# mcp4728._channel_b_multi_write = 0b0000111111111111
# mcp4728._channel_c_multi_write = 0b0000111111111111 
# mcp4728._channel_d_multi_write = 0b0000111111111111

# mcp4728.write_multi_eeprom([
#     0b00001111, 0b11111111,
#     0b00001111, 0b11111111,
#     0b00001111, 0b11111111,
#     0b00001111, 0b11111111
# ])
EEPROM_WAIT = 0.015 # 100ms
time.sleep(0.100)
# print_regs()

mcp4728.read_registers()

time.sleep(2)
val = 0b111000000111
val = 0
mcp4728._channel_d_single_write_eeprom = 0b1110111100000000
time.sleep(EEPROM_WAIT)
mcp4728._channel_c_single_write_eeprom = 99 
time.sleep(EEPROM_WAIT)
mcp4728._channel_b_single_write_eeprom = 102
time.sleep(EEPROM_WAIT)
mcp4728._channel_a_single_write_eeprom = 1234
time.sleep(EEPROM_WAIT)

mcp4728.read_registers()
# mcp4728.channel_a = 0b0000110011001100 # Voltage = VCC
# mcp4728.channel_b = 0b0000110011001100
# mcp4728.channel_c = 0b0000110011001100 
# mcp4728.channel_d = 0b0000110011001100
