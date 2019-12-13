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

* Adafruit's MCP4728 Breakout: https://adafruit.com/product/44XX

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards: https://circuitpython.org/downloads
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP4728.git"

from struct import pack_into
from time import sleep
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import UnaryStruct
import traceback

_MCP4728_DEFAULT_ADDRESS = 0x60

_MCP4728_CH_A_MULTI_IB = 0x40
_MCP4728_CH_B_MULTI_IB = 0x42
_MCP4728_CH_C_MULTI_IB = 0x44
_MCP4728_CH_D_MULTI_IB = 0x46

_MCP4728_CH_A_SINGLE_EEPROM = 0x58
_MCP4728_CH_B_SINGLE_EEPROM = 0x5A
_MCP4728_CH_C_SINGLE_EEPROM = 0x5C
_MCP4728_CH_D_SINGLE_EEPROM = 0x5E

_MCP4728_CH_A_MULTI_EEPROM = 0x50

class CV:
    """struct helper"""

    @classmethod
    def add_values(cls, value_tuples):
        "creates CV entires"
        cls.string = {}
        cls.lsb = {}

        for value_tuple in value_tuples:
            name, value, string, lsb = value_tuple
            setattr(cls, name, value)
            cls.string[value] = string
            cls.lsb[value] = lsb

    @classmethod
    def is_valid(cls, value):
        "Returns true if the given value is a member of the CV"
        return value in cls.string

class Vref(CV):
    """Options for ``vref``"""
    pass #pylint: disable=unnecessary-pass

Vref.add_values((
    ('VDD', 0, "VDD", None),
    ('INTERNAL', 1, "Internal 2.048V", None),
))

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
        
        raw_registers = self._read_registers()

        self.channel_a = Channel(self, self._cache_page(*raw_registers[0]), 0)
        self.channel_b = Channel(self, self._cache_page(*raw_registers[1]), 1)
        self.channel_c = Channel(self, self._cache_page(*raw_registers[2]), 2)
        self.channel_d = Channel(self, self._cache_page(*raw_registers[3]), 3)

    def _get_flags(self, high_byte):
        vref = (high_byte & 1<<7) > 0
        gain = (high_byte & 1<<4) > 0
        pd = (high_byte & 0b011<<5)>>5
        return (vref, gain, pd)

    def _cache_page(self, value, vref, gain, pd):
        return {"value": value, "vref": vref, "gain": gain, "pd": pd}

    def _read_registers(self):
        buf = bytearray(24)

        with self.i2c_device as i2c:
            i2c.readinto(buf)

        self._print_buffer(buf)

        # stride is 6 because we get 6 bytes for each channel; 3 for the output regs
        # and 3 for the eeprom. here we only care about the output buffer so we throw out
        # the eeprom values as 'n/a'
        current_values = []
        for header, high_byte, low_byte, na_1, na_2, na_3 in self._chunk(buf, 6):
            value = (high_byte & 0b00001111) << 8 | low_byte
            vref, gain, pd = self._get_flags(high_byte)
            current_values.append((value, vref, gain, pd))

        return current_values

    def _print_buffer(self, buf):
        print()
        for index, value in enumerate(buf):
            if index %3 == 0:
                print("\n%4s\t"%index, end="")
            print("%s %s "%(format(value, '#010b'), hex(value)), end="")
        print()


    def save_settings(self):
        """Saves the currently selected values, Vref, and gain selections for each channel to the EEPROM, setting them as defaults on power up"""
        byte_list = []
        byte_list += self._generate_bytes_with_flags(self.channel_a)
        byte_list += self._generate_bytes_with_flags(self.channel_b)
        byte_list += self._generate_bytes_with_flags(self.channel_c)
        byte_list += self._generate_bytes_with_flags(self.channel_d)
        self._write_multi_eeprom(byte_list)

    # TODO: add the ability to set an offset
    def _write_multi_eeprom(self, byte_list):
        buffer_list = [_MCP4728_CH_A_MULTI_EEPROM]
        buffer_list += byte_list

        buf = bytearray(buffer_list)
        self._print_buffer(buf)
        with self.i2c_device as i2c:
            i2c.write(buf)

        sleep(0.015) # the better to write you with

    def _sync_vrefs(self):
        base_values = 0b10000000
        base_values |= (self.channel_a.vref<<3)
        base_values |= (self.channel_b.vref<<2)
        base_values |= (self.channel_c.vref<<1)
        base_values |= (self.channel_d.vref)
        
        print("vref values:")
        print(base_values)
        print(self._lzb(base_values))

        buf = bytearray(1)
        pack_into(">B", buf, 0, base_values)        
        print("buf bytes:")
        self._print_buffer(buf)
        with self.i2c_device as i2c:
            i2c.write(buf)

    def _sync_gains(self):
        # [S] 1 1 0 0 A2 A1 A0 0 
        # [A] 1 1 0 X GXA GXB GXC GXD [A] [P]
        base_values = 0b11000000
        base_values |= (self.channel_a.gain<<3)
        base_values |= (self.channel_b.gain<<2)
        base_values |= (self.channel_c.gain<<1)
        base_values |= (self.channel_d.gain)


        print("gain values:")
        print(base_values)
        print(self._lzb(base_values))

        buf = bytearray(1)
        pack_into(">B", buf, 0, base_values)        
        print("buf bytes:")
        self._print_buffer(buf)

        with self.i2c_device as i2c:
            i2c.write(buf)

    def _set_value(self, channel):

        channel_bytes = self._generate_bytes_with_flags(channel)

        write_command_byte = 0b01000000 # 0 1 0 0 0 DAC1 DAC0 UDAC
        write_command_byte |= (channel._channel_index<<1)

        channel_bytes.insert(0, write_command_byte)

        with self.i2c_device as i2c:
            i2c.write(bytearray(channel_bytes))

    def _generate_bytes_with_flags(self, channel):
        buf = bytearray(2)
        pack_into(">H", buf, 0, channel.raw_value)

        buf[0] |= channel.vref << 7
        buf[0] |= channel.gain << 4

        return buf

    def _chunk(self, l, n):
        # For item i in a range that is a length of l,
        for i in range(0, len(l), n):
            # Create an index range for l of n items:
            yield l[i:i+n]

    def _lzb(self, byte_val): # leading zero bin
        return format(byte_val, '#010b')
    def _bt(self):
        for line in traceback.format_stack():
            print(line.strip())
class Channel:
    """An instance of a single channel for a multi-channel DAC"""
    def __init__(self, dac_instance, cache_page, index):
        self._vref = cache_page['vref']
        self._gain = cache_page['gain']
        self._raw_value = cache_page['value']
        self._dac = dac_instance
        self._channel_index = index

    @property
    def normalized_value(self):
        """The DAC value as a floating point number in the range 0.0 to 1.0."""
        return self.raw_value / (2**12-1)

    @normalized_value.setter
    def normalized_value(self, value):
        if value < 0.0 or value > 1.0:
            raise AttributeError("`normalized_value` must be between 0.0 and 1.0")

        self.raw_value = int(value * 4095.0)

    @property
    def value(self):
        """The 16-bit scaled current value for the channel. Note that the MCP4728 is a 12-bit piece
        so quantization errors will occour"""
        return self.normalized_value * (2**16-1)

    @value.setter
    def value(self, value):
        if value < 0 or value > (2**16-1):
            raise AttributeError("`value` must be a 16-bit integer between 0 and %s"%(2**16-1))

        # Scale from 16-bit to 12-bit value (quantization errors will occur!).
        self.raw_value = value >> 4

    @property
    def raw_value(self):
        """The native 12-bit value used by the DAC"""
        return self._raw_value

    @raw_value.setter
    def raw_value(self, value):
        if value < 0 or value > (2**12-1):
            raise AttributeError("`raw_value` must be a 12-bit integer between 0 and %s"%(2**12-1))
        self._raw_value = value
        self._dac._set_value(self)

    @property
    def gain(self):
        """Sets the gain of the channel if the Vref for the channel is ``Vref.INTERNAL``. *The gain setting has no effect if the Vref for the channel is `Vref.VDD`*. With gain set to 1, the output voltage goes from 0v to 2.048V. If a channe's gain is set to 2, the voltage goes from 0v to 4.096V. `gain` Must be 1 or 2"""
        return self._gain

    @gain.setter
    def gain(self, value):
        if value != 1 and value != 2:
            raise AttributeError("`gain` must be 1 or 2")
        self._gain = value-1
        self._dac._sync_gains()

    @property
    def vref(self):
        """Sets the DAC's voltage reference source. Must be a ``VREF``"""
        return self._vref

    @vref.setter
    def vref(self, value):
        if not Vref.is_valid(value):
            raise AttributeError("range must be a `Vref`")
        self._vref = value
        self._dac._sync_vrefs()
