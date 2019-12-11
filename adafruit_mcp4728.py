# The MIT License (MIT)
#
# Copyright (c) 2019 Bryan Siepert for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_mcp4728`
================================================================================

Helper library for the Microchip MCP4728 I2C 12-bit Quad DAC


* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

.. todo:: Update the PID for the below and add links to any specific hardware product page(s), or category page(s)
* Adafruit's MCP4728 Breakout: https://adafruit.com/product/44XX

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards: https://circuitpython.org/downloads
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP4728.git"

from time import sleep
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_struct_array import StructArray
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_bits import RWBits

_MCP4728_DEFAULT_ADDRESS = 0x60 

"""
# DAC1, DAC0 DAC Channel Selection bits:
# 00 = Channel A
# 01 = Channel B
# 10 = Channel C
# 11 = Channel D

0 = slave addr(auto)
0 1 0 0 0 DAC1 DAC0 UDAC[A]
01000 + 00 + UDAC = 
0b01000000 = 0x40 (+2 for each successive)
VREF PD1 PD0 Gx D11 D10 D9 D8 [A]
D7 D6 D5 D4 D3 D2 D1 D0 [A]

0 1 0 0 0 Multi-Write for DAC
0 1 0 1 0 Sequential Write for DAC Input Registers and EEPROM
0 1 0 1 1 Single Write for DAC Input Register and EEPROM

1 0 0 0 0 Write Reference (VREF) selection bits to Input Registers
1 1 0 0 0 Write Gain selection bits to Input Registers
1 0 1 0 0 Write Power-Down bits to Input Registers
"""

'0b 010 00 000'
_MCP4728_CH_A_MULTI_IB = 0x40
_MCP4728_CH_B_MULTI_IB = 0x42
_MCP4728_CH_C_MULTI_IB = 0x44
_MCP4728_CH_D_MULTI_IB = 0x46

'0b 010 11 000'
_MCP4728_CH_A_SINGLE_EEPROM = 0x58
_MCP4728_CH_B_SINGLE_EEPROM = 0x5A
_MCP4728_CH_C_SINGLE_EEPROM = 0x5C
_MCP4728_CH_D_SINGLE_EEPROM = 0x5E

'0b 010 10 000'
_MCP4728_CH_A_MULTI_EEPROM = 0x50

class MCP4728:
    """Helper library for the Microchip MCP4728 I2C 12-bit Quad DAC.

        :param ~busio.I2C i2c_bus: The I2C bus the MCP4728 is connected to.
        :param address: The I2C slave address of the sensor

    """
    _channel_a_single_write_eeprom = UnaryStruct(_MCP4728_CH_A_SINGLE_EEPROM, ">H")
    _channel_b_single_write_eeprom = UnaryStruct(_MCP4728_CH_B_SINGLE_EEPROM, ">H")
    _channel_c_single_write_eeprom = UnaryStruct(_MCP4728_CH_C_SINGLE_EEPROM, ">H")
    _channel_d_single_write_eeprom = UnaryStruct(_MCP4728_CH_D_SINGLE_EEPROM, ">H") 

    _channel_a_multi_write = UnaryStruct(_MCP4728_CH_A_MULTI_IB, ">H")
    _channel_b_multi_write = UnaryStruct(_MCP4728_CH_B_MULTI_IB, ">H")
    _channel_c_multi_write = UnaryStruct(_MCP4728_CH_C_MULTI_IB, ">H")
    _channel_d_multi_write = UnaryStruct(_MCP4728_CH_D_MULTI_IB, ">H")

    _multi_write_channel_a_start = UnaryStruct(_MCP4728_CH_A_MULTI_EEPROM, ">HHHH")

    def __init__(self, i2c_bus, address=_MCP4728_DEFAULT_ADDRESS):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

    @property
    def channel_a(self):
        """channel a's current value"""
        return "hamsters"
    
    @channel_a.setter
    def channel_a(self, value):
        self._channel_a_multi = value


    @property
    def channel_b(self):
        """channel b's current value"""
        return "elves"
    
    @channel_b.setter
    def channel_b(self, value):
        self._channel_b_multi = value

    @property
    def channel_c(self):
        """channel c's current value"""
        return "pancakes"
    
    @channel_c.setter
    def channel_c(self, value):
        self._channel_c_multi = value

    @property
    def channel_d(self):
        """channel d's current value"""
        return "gummies"
    
    @channel_d.setter
    def channel_d(self, value):
        self._channel_d_multi = value


    def write_init(self, register_address, struct_format):
        self.format = struct_format
        self.address = register_address

    # def read(self, obj):
    #     buf = bytearray(1+struct.calcsize(self.format))
    #     buf[0] = self.address
    #     with self.i2c_device as i2c:
    #         i2c.write_then_readinto(buf, buf, out_end=1, in_start=1)
    #     return struct.unpack_from(self.format, buf, 1)[0]

    # def write(self, obj, value):
    #     buf = bytearray(1+struct.calcsize(self.format))
    #     buf[0] = self.address
    #     struct.pack_into(self.format, buf, 1, value)
    #     with self.i2c_device as i2c:
    #         i2c.write(buf)
    def chunks(self, l, n):
        # For item i in a range that is a length of l,
        for i in range(0, len(l), n):
            # Create an index range for l of n items:
            yield l[i:i+n]

    def get_flags(self, high_byte):
        vref = (high_byte & 1<<7) > 0
        gain = (high_byte & 1<<4) > 0
        pd = (high_byte & 0b011<<5)>>5
        return (vref, gain, pd)

    def read_registers(self):
        buf = bytearray(24)

        with self.i2c_device as i2c:
            i2c.readinto(buf)
        index = 0
        for index, value in enumerate(buf):
            if index %3 is 0:
                print("\n%4s\t"%index, end="")
            print("%s %s "%( format(value, '#010b'), hex(value)), end="")
        print()
        # stride is 6 because we get 6 bytes for each channel; 3 for the output regs 
        # and 3 for the eeprom. here we only care about the output buffer
        current_values = []
        for header, high_byte, low_byte, na_1, na_2, na_3 in self.chunks(buf,6):
            value = (high_byte & 0b00001111) << 8 | low_byte
            vref, gain, pd = self.get_flags(high_byte)
            current_values << (value, vref, pd, gain)

        return current_values
        # ch_a_header, ch_a_hb, ch_a_lb = buf[0:3]
        # ch_aee_header, ch_aee_hb, ch_aee_lb = buf[3:6]
        # # ch_c_header, ch_c_hb, ch_c_lb = buf[6:9]
        # # ch_d_header, ch_d_hb, ch_d_lb = buf[9:12]

        # ch_a_val = 

        # print("%s %s %s"%( self.b(ch_a_header),self.b(ch_a_hb), self.b(ch_a_lb) ))
        # print("%s %s %s"%( self.b(ch_b_header),self.b(ch_b_hb), self.b(ch_b_lb) ))
        # # print("%s %s %s"%( self.b(ch_c_header),self.b(ch_c_hb), self.b(ch_c_lb) ))
        # # print("%s %s %s"%( self.b(ch_d_header),self.b(ch_d_hb), self.b(ch_d_lb) ))

    def b(self, byte_val):
        return format(byte_val, '#010b')

    def write_multi_eeprom(self, byte_list, start=0):
        buffer_list = [_MCP4728_CH_A_MULTI_EEPROM]
        buffer_list += byte_list
        print("Byte List:")
        print(buffer_list)
        buf = bytearray(buffer_list)
        # struct.pack_into(self.format, buf, 1, value)
        with self.i2c_device as i2c:
            i2c.write(buf)



        


    @property
    def ch_a(self):
        return "poo"

    @ch_a.setter
    def ch_a(self, value):
        self._channel_a_multi = value

"""
# set the gain for a channel
    cache each, set all?

# set reference source for a channel
    cache each, set all?

# save settings to eeprom

# write a channel 

# write all channels

# latching?
"""