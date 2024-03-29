
import time
import logging
from threading import Thread

from LedStrip import LedStrip
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
        self.led_strip = LedStrip()
        
        self.herzschlagvalue_stack = []
        


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


    def plot_herzschlag(self, value):
        log.info(f"max: {value}  {(value-10000)//300 * '#'} \r")
        self.alarm_led.blink()

    def send_herzschlag(self, value_stack: list):
        telemetry = {"herzschlag": value_stack}
        s={
            "ts": 1711718630775,
            "values": {
                "temperature": 42.2,
            }
        }

        thingsboard.send(telemetry)
        
        
    def show_herzschlag_on_strip(self, current_value: int):
        self.led_strip.on_receive_herzschlag_value(current_value)


    def start_herzschlag_messung(self):
        self.herzschlag_messer = HerzschlagMessung(self.plot_herzschlag)
        herzschlag_thread = Thread(target=self.herzschlag_messer_thread)
        herzschlag_thread.start()
        
    def save_new_herzschlag_value(self, current_value: int):
        """Jeder neue Wert wird gespeichert. Wenn der Speicher 10 Werte ueberschreitet 
        werden die Daten gebuendelt Thingsboard uebermittelt und den Speicher geloescht."""
        current_time = time.time()
        self.herzschlagvalue_stack.append([current_time, current_value])
        
        if len(self.herzschlagvalue_stack) > 10:
            self.send_herzschlagvalue_stack(self.herzschlagvalue_stack)
            self.herzschlagvalue_stack.clear()
    
    def send_herzschlagvalue_stack(self, value_stack: list):
        pass
         
    def herzschlag_messer_thread(self):
        try:
            while True:
                current_herzschlag_value = self.herzschlag_messer.abtastung()
                self.show_herzschlag_on_strip(current_herzschlag_value)
                self.save_new_herzschlag_value(current_herzschlag_value)

                time.sleep(self.herzschlag_messer.ABTASTRATE)
            
        except KeyboardInterrupt | SystemExit:
            log.info("Clearing LED1")
            self.alarm_led.off()
            self.led_strip.clear()
            
    def __del__(self):
        log.info("Clearing LED2")
        self.alarm_led.off()
        self.led_strip.clear()
        




if __name__ == "__main__":
    
    artz = Arzt()
    artz.start_herzschlag_messung()
    del artz