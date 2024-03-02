from ThingsBoardConnection import ThingsBoard

import time
import logging


def fk(args):
    logging.info(f"antwort: {args=}")



if __name__ == "__main__":

    thingsboard = ThingsBoard()

    thingsboard.subscribe_to_attribute("enabled", fk)
    time.sleep(2)
    time.sleep(5)
