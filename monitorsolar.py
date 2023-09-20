import datetime
import time

import board
from adafruit_ina219 import INA219

i2c_bus = board.I2C()  # uses board.SCL and board.SDA

ina219 = INA219(i2c_bus)

while True:
    timenow = datetime.datetime.now().astimezone().strftime('%Y/%m/%d-%H:%M:%S')
    voltage = ina219.bus_voltage + ina219.shunt_voltage  # Voltage of the power source
    current = ina219.current  # current in mA
    power = ina219.power  # power in watts

    print(f'{voltage:2.04f} V, {current:4.01f} mA, {power:1.03f} W\n')
    time.sleep(1)
