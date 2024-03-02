# coding=utf-8
 
#############################################################################################################
### Copyright by Joy-IT
### Published under Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License
### Commercial use only after permission is requested and granted
###
### KY-053 Analog Digital Converter - Raspberry Pi Python Code Example
###
#############################################################################################################
import time
import board
import busio
import logging
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import dotenv
import os
from tb_device_mqtt import TBDeviceMqttClient


dotenv.load_dotenv()
    
logging.info(f"Stelle Verbindung zum Bakcend her: mqtt://{os.environ['TB_HOST']}:{os.environ['TB_PORT']}")

tb_client = TBDeviceMqttClient(
        host = os.environ["TB_HOST"],
        port = int(os.environ["TB_PORT"]),
        username = os.environ["TB_TOKEN"]
    )
    
tb_client.connect()

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

while True:
    print("channel 0: ","{:>5}\t{:>5.3f}".format(chan0.value, chan0.voltage))
    
    tb_client.send_telemetry({"Value": chan0.value})
    
    time.sleep(.01)