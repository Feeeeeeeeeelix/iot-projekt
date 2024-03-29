
import time
import logging
import LedStrip
from BlinkLED import LED
from TemperaturSensor import TemperaturSensor
from Herzschlag import HerzschlagMessung
from ThingsBoardConnection import ThingsBoard



logging.basicConfig(
    format = "%(asctime)s - %(levelname)s - %(message)s",
    level = logging.DEBUG,
)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Arzt:
    def __init__(self) -> None:

        self.thingsboard_client = ThingsBoard()
        self.alarm_led = LED()


    def schalte_temperaturalarm(self, alarmzustand: bool):
        pass

    def werteTemperaturAus(self):

        temperatur_sensor = TemperaturSensor(self.schalte_temperaturalarm)
        try:
            while True:
                temp = temperatur_sensor.get_temperature()
                
                log.info("Temperatur:",temp , "degC \r")
                if temp:
                    self.thingsboard_client.send({"temperatuuur": temp})
                    
                temperatur_sensor.wait()
                
        except KeyboardInterrupt:
            led.off()


    def plot_herzschlag(value):
        log.info(f"max: {value}  {(value-10000)//300 * '#'} \r")
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
        
        
    def show_herzschlag_on_strip(current_value: int):
        LedStrip.on_receive_herzschlag_value(current_value)

    def werteHerzschlagAus(self):
        herzschlagmesser = HerzschlagMessung()
        try:
            herzschlagmesser.erkenne_maximum()
        except KeyboardInterrupt:
            led.off()




if __name__ == "__main__":
    
    artz = Arzt()