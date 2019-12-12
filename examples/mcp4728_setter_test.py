import board
import busio
import adafruit_mcp4728

i2c = busio.I2C(board.SCL, board.SDA)
mcp4728 =  adafruit_mcp4728.MCP4728(i2c)

# mcp4728.channel_a.value = 0 # Voltage = VCC
# mcp4728.channel_b.value = 50 # VCC/2
# mcp4728.channel_c.value = 100 # VCC/4
# mcp4728.channel_d.value = 65535  # VCC/8

# mcp4728.channel_a.gain = 2
# mcp4728.channel_b.gain = 2
# mcp4728.channel_c.gain = 2
# mcp4728.channel_d.gain = 2

# mcp4728.channel_a.vref = 0
# mcp4728.channel_b.vref = 0
# mcp4728.channel_c.vref = 0
# mcp4728.channel_d.vref = 0

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
print("cha vref:", mcp4728.channel_a.vref)
print("chb vref:", mcp4728.channel_b.vref)
print("chc vref:", mcp4728.channel_c.vref)
print("chd vref:", mcp4728.channel_d.vref)


# mcp4728.save_settings()