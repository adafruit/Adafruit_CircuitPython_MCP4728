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

Helper library for the TI MCP4728 I2C 12-bit Quad DAC


* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

.. todo:: Update the PID for the below and add links to any specific hardware product page(s), or category page(s)
* Adafruit's MCP4728 Breakout: https://adafruit.com/product/44XX

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MCP4728.git"'BusDevice': ('https://circuitpython.readthedocs.io/projects/busdevice/en/latest/', None),'Register': ('https://circuitpython.readthedocs.io/projects/register/en/latest/', None),# Common imports; remove if unused or pylint will complain
from time import sleepimport adafruit_bus_device.i2c_device as i2c_devicefrom adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_struct_array import StructArray
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_bits import RWBits_MCP4728_DEFAULT_ADDRESS) = 0x00 # MCP4728 default i2c address
_MCP4728_DEVICE_ID = 0xFF # MCP4728 device identifier

class MCP4728:
    """Helper library for the TI MCP4728 I2C 12-bit Quad DAC.

        :param ~busio.I2C i2c_bus: The I2C bus the MCP4728 is connected to.
        :param address: The I2C slave address of the sensor

    """
    _device_id = ROUnaryStruct(_MCP4728_DEVICE_ID, ">B")

    def __init__(self, i2c_bus, address=_MCP4728_DEFAULT_ADDRESS):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        if self._device_id != _MCP4728_DEVICE_ID:
            raise RuntimeError("Failed to find MCP4728 - check your wiring!")

        self.reset()
