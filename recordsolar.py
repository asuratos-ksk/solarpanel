import datetime
import os

import board
import boto3
from adafruit_ina219 import INA219
from dotenv import main as dotenv

i2c_bus = board.I2C()  # uses board.SCL and board.SDA

ina219 = INA219(i2c_bus)

dotenv.load_dotenv()

s3_access_key = os.environ.get('S3ACCESSKEY')
s3_secret_key = os.environ.get('S3SECRETKEY')
location = os.environ.get('LOCATION')

filename = f'solar-{location}-{datetime.datetime.now().strftime("%Y%m%d")}.csv'
targetdir = f'{os.path.dirname(os.path.abspath(__file__))}/data'
target = f'{targetdir}/{filename}'


if not os.path.exists(target):
    if not os.path.exists(targetdir):
        os.mkdir(targetdir)
    with open(target, "a") as f:
        f.write("timestamp,voltage,current,power\n")

with open(target, "a+") as f:
    timenow = datetime.datetime.now().astimezone().strftime('%Y/%m/%d-%H:%M:%S')
    voltage = ina219.bus_voltage + ina219.shunt_voltage  # Voltage of the power source
    current = ina219.current  # current in mA
    power = ina219.power  # power in watts
    f.write(f"{timenow},{voltage:.05f},{current:4.02f},{power:.03f}\n")


with open(file=target, mode='rb') as f:
    bucket_name = 'tsutsui-test'
    s3 = boto3.client(
        "s3", aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key
    )

    s3.put_object(Bucket=bucket_name, Body=f, Key=filename)
