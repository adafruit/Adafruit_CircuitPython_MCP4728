import time
import board
import busio
import adafruit_mcp4728
import math
i2c = busio.I2C(board.SCL, board.SDA, frequency=3200000)

mcp4728 =  adafruit_mcp4728.MCP4728(i2c)

def sin_2_bits(sin_val):
    raw_bits = sin_val * 2048
    raw_bits += 2048
    if raw_bits < 0:
        raw_bits = 0
    if raw_bits > 4095:
        raw_bits = 4095
    print("Raw bits:", raw_bits)
    return int(raw_bits)

bits = 0
bits_array = []
for i in range(0,45):
    bits = sin_2_bits(math.sin(math.radians(i*8)))
    bits_array.append(bits)

while True:
    for i in range(0,10000):
        bits = bits_array[i%45]
        mcp4728.ch_a = bits
        # mcp4728.channel_b = bits
        # mcp4728.channel_c = bits
        # mcp4728.channel_d = bits
        # print(bits)
        # mcp4728.channel_b = bits
