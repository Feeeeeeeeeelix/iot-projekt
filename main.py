from ThingsBoardConnection import ThingsBoard

import time
import logging
import TemperaturSensor


def fk(args):
    logging.info(f"antwort: {args=}")

def main(tb:ThingsBoard):

    TemperaturSensor.setup()
    TemperaturSensor.TemperaturMessung()
    while True:
        print ("---------------------------------------")
        temp = TemperaturSensor.TemperaturAuswertung()
        print ("Temperatur:",temp , "degC")
        if temp:
            tb.send({"temperatuuur": temp})
        time.sleep(TemperaturSensor.sleeptime)


if __name__ == "__main__":
    thingsboard = ThingsBoard()
    
    main(thingsboard)

    # thingsboard.subscribe_to_attribute("enabled", fk)
    # time.sleep(2)
    # time.sleep(5)
