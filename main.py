from ThingsBoardConnection import ThingsBoard

import time
import logging
import TemperaturSensor
import Herzschlag
from KY001_LED import LED

global led
led = LED()

logging.basicConfig(
    format = "%(asctime)s - %(levelname)s - %(message)s",
    level = logging.INFO,
)

def fk(args):
    logging.info(f"antwort: {args=}")

def werteTemperaturAus(tb:ThingsBoard):

    TemperaturSensor.setup()
    TemperaturSensor.TemperaturMessung()
    try:
        while True:
            temp = TemperaturSensor.TemperaturAuswertung()
            
            print ("Temperatur:",temp , "degC \r")
            if temp:
                tb.send({"temperatuuur": temp})
                
            time.sleep(TemperaturSensor.sleeptime)
    except KeyboardInterrupt:
        led.off()


def plot_herzschlag(value):
    logging.info(f"max: {value}  {(value-10000)//300 * '#'} \r")
    led.blink()

def send_herzschlag(value_stack: list):
    telemetry = {"herzschlag": value_stack}
    s={
        "ts": 1711718630775,
        "values": {
            "temperature": 42.2,
        }
    }

    thingsboard.send(telemetry)

def werteHerzschlagAus(tb: ThingsBoard):
    h = Herzschlag.HerzschlagMessung(plot_herzschlag, send_herzschlag)
    try:
        h.erkenne_maximum()
    except KeyboardInterrupt:
        led.off()




if __name__ == "__main__":
    
    thingsboard = ThingsBoard()
    
    # werteTemperaturAus(thingsboard)
    
    werteHerzschlagAus(thingsboard)

    # thingsboard.subscribe_to_attribute("enabled", fk)
    # time.sleep(2)
    # time.sleep(5)
