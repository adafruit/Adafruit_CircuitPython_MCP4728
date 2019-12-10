import time
import board
import busio
import adafruit_mcp4728

i2c = busio.I2C(board.SCL, board.SDA)

mcp4728 =  adafruit_mcp4728.MCP4728(i2c)

# while True:
    # pass
