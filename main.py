from ThingsBoardConnection import ThingsBoard

import time
import logging
import TemperaturSensor
import Herzschlag


logging.basicConfig(
    format = "%(asctime)s - %(levelname)s - %(message)s",
    level = logging.INFO,
)

def fk(args):
    logging.info(f"antwort: {args=}")

def werteTemperaturAus(tb:ThingsBoard):

    TemperaturSensor.setup()
    TemperaturSensor.TemperaturMessung()
    while True:
        temp = TemperaturSensor.TemperaturAuswertung()
        print ("Temperatur:",temp , "degC \r")
        if temp:
            tb.send({"temperatuuur": temp})
        time.sleep(TemperaturSensor.sleeptime)


def plot_herzschlag(value):
    logging.info(f"max: {value}  {(value-10000)//300 * '#'} \r")

def werteHerzschlagAus(tb: ThingsBoard):
    h = Herzschlag.HerzschlagMessung(plot_herzschlag)
    h.erkenne_maximum()
    

if __name__ == "__main__":
    
    thingsboard = ThingsBoard()
    
    # werteTemperaturAus(thingsboard)
    
    werteHerzschlagAus(thingsboard)

    # thingsboard.subscribe_to_attribute("enabled", fk)
    # time.sleep(2)
    # time.sleep(5)
