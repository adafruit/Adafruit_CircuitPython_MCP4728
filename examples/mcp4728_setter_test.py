import board
import busio
import adafruit_mcp4728
from adafruit_mcp4728 import Vref
import digitalio
i2c = busio.I2C(board.SCL, board.SDA)
mcp4728 =  adafruit_mcp4728.MCP4728(i2c)

mcp4728.channel_a.value = 32768 # Voltage = VCC
mcp4728.channel_b.value = 32768 # VCC/2
mcp4728.channel_c.value = 32768 # VCC/4
mcp4728.channel_d.value = 32768 # VCC/8


mcp4728.channel_a.gain = 1
mcp4728.channel_b.gain = 2
mcp4728.channel_c.gain = 1
mcp4728.channel_d.gain = 2

mcp4728.channel_a.vref = Vref.INTERNAL
mcp4728.channel_b.vref = Vref.INTERNAL
mcp4728.channel_c.vref = Vref.INTERNAL
mcp4728.channel_d.vref = Vref.INTERNAL

print("cha raw value:", mcp4728.channel_a.raw_value)
print("chb raw value:", mcp4728.channel_b.raw_value)
print("chc raw value:", mcp4728.channel_c.raw_value)
print("chd raw value:", mcp4728.channel_d.raw_value)
print()
print("cha value:", mcp4728.channel_a.value)
print("chb value:", mcp4728.channel_b.value)
print("chc value:", mcp4728.channel_c.value)
print("chd value:", mcp4728.channel_d.value)
print()

print("cha gain:", mcp4728.channel_a.gain)
print("chb gain:", mcp4728.channel_b.gain)
print("chc gain:", mcp4728.channel_c.gain)
print("chd gain:", mcp4728.channel_d.gain)
print()
print("cha vref:", Vref.string[mcp4728.channel_a.vref])
print("chb vref:", Vref.string[mcp4728.channel_b.vref])
print("chc vref:", Vref.string[mcp4728.channel_c.vref])
print("chd vref:", Vref.string[mcp4728.channel_d.vref])

mcp4728._read_registers()

print("saving regs")
mcp4728.save_settings()
mcp4728._read_registers()
