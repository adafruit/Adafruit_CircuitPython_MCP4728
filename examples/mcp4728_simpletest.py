import board
import busio
import adafruit_mcp4728

i2c = busio.I2C(board.SCL, board.SDA)
mcp4728 =  adafruit_mcp4728.MCP4728(i2c)

mcp4728.channel_a.value = 4095 # Voltage = VCC
mcp4728.channel_b.value = 2048 # VCC/2
mcp4728.channel_c.value = 1024 # VCC/4
mcp4728.channel_d.value = 512  # VCC/8
