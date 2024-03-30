
import time
import logging
import schedule
from threading import Thread

from LedStrip import LedStrip
from BlinkLED import LED
from Buzzer import Buzzer
from TemperaturSensor import TemperaturSensor
from Herzschlag import HerzschlagMessung
from ThingsBoardConnection import ThingsBoard



logging.basicConfig(
    format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level = logging.DEBUG,
)

log = logging.getLogger("Arzt")
log.setLevel(logging.INFO)


class Arzt:
    TEMP_ALARM_ATTR = "temperature_alarm"
    PULSE_ALARM_ATTR = "pulse_alarm"
    BUZZER_STATE = "buzzer-enabled"
    
    TEMP_TELEMETRY = "temperature"
    PULS_TELEMETRY = "pulse"
    
    def __init__(self) -> None:

        self.thingsboard_client = ThingsBoard()
        self.alarm_led = LED()
        self.led_strip = LedStrip()
        self.buzzer = Buzzer()
        
        self.herzschlagvalue_stack = []
        
        self.temp_alarm = False
        self.puls_alarm = False
        self.buzzer_enabled = True
        
        self.thingsboard_client.set_callback_for_rpc_request(self.BUZZER_STATE, self.on_receive_buzzer_state)
    
    def on_receive_buzzer_state(self, state):
        log.info(f"received update for buzzer state: {state}")
        self.buzzer_enabled = state 


    def schalte_temperaturalarm(self, alarmzustand: bool):
        log.info(f"Temperatur Alarm: {alarmzustand}")
        self.temp_alarm = alarmzustand
        self.thingsboard_client.set_attribute(self.TEMP_ALARM_ATTR, alarmzustand)
    
    def send_temperature(self, temperature: float):
        log.info(f"Send Temperature: {temperature}°C")
        if temperature:
            self.thingsboard_client.send({self.TEMP_TELEMETRY: temperature})

    def temp_auswertung_thread(self):
        try:
            while True:
                temp = self.temperatur_sensor.get_temperature()
                
                self.send_pulse()
                self.send_temperature(temp)
                time.sleep(self.temperatur_sensor.ABTASTRATE)
                
        except KeyboardInterrupt:
            del self
    
    def on_receive_alarm(self, alarm_state: bool):
        log.warning(f"Alarm state: {alarm_state}")
        
        if alarm_state and self.buzzer_enabled:
            self.buzzer.SOS()
    
    def start_temperatur_auswertung(self):

        self.temperatur_sensor = TemperaturSensor(self.schalte_temperaturalarm)
        temp_thread = Thread(target=self.temp_auswertung_thread)
        temp_thread.start()
        
        self.thingsboard_client.subscribe_to_attribute(self.TEMP_ALARM_ATTR, self.on_receive_alarm)
        self.thingsboard_client.subscribe_to_attribute(self.PULSE_ALARM_ATTR, self.on_receive_alarm)





    def plot_herzschlag(self, value):
        log.debug(f"max: {value}  {(value-10000)//300 * '#'} \r")
        self.alarm_led.blink()

    def send_pulse(self):
        if self.herzschlag_messer:
            if puls := self.herzschlag_messer.puls:
                telemetry = {self.PULS_TELEMETRY: puls}

                log.info(f"{puls=}")
                self.thingsboard_client.send(telemetry)
        
        
    def show_herzschlag_on_strip(self, current_value: int):
        self.led_strip.on_receive_herzschlag_value(current_value)

        
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
                # self.save_new_herzschlag_value(current_herzschlag_value)

                time.sleep(self.herzschlag_messer.ABTASTRATE)
            
        except KeyboardInterrupt | SystemExit:
            log.warning("Clearing LED1")
            del self

    def start_herzschlag_messung(self):
        self.herzschlag_messer = HerzschlagMessung(self.plot_herzschlag)
        herzschlag_thread = Thread(target=self.herzschlag_messer_thread)
        herzschlag_thread.start()
            
            
    def __del__(self):
        log.warning("Clearing LED2")
        self.alarm_led.off()
        self.led_strip.clear()
        




if __name__ == "__main__":
    
    artz = Arzt()
    artz.start_temperatur_auswertung()
    artz.start_herzschlag_messung()
    del artz