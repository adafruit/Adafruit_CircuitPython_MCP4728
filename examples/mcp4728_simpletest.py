import board
import busio
import adafruit_mcp4728

i2c = busio.I2C(board.SCL, board.SDA)
mcp4728 =  adafruit_mcp4728.MCP4728(i2c)

mcp4728.channel_a.value = 65535 # Voltage = VDD
mcp4728.channel_b.value = int(65535/2) # VDD/2
mcp4728.channel_c.value = int(65535/4) # VDD/4
mcp4728.channel_d.value = 0 # 0V


mcp4728.save_settings() # save the current values to the eeprom,making them the default on power up
