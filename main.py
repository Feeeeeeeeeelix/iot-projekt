
import time
import logging
import signal
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
        self.herzschlag_messer = None
        
        self.herzschlagvalue_stack = []
        
        self.temp_alarm = False
        self.puls_alarm = False
        self.buzzer_enabled = True
        
        self.thingsboard_client.set_attribute(self.BUZZER_STATE, True)
        self.thingsboard_client.set_callback_for_rpc_request(self.BUZZER_STATE, self.on_receive_buzzer_state)
        
        self.herzschlagmesser_thread_active = True
        self.temp_thread_active = True
        signal.signal(signal.SIGINT, self.interrupt_signal_handler)
    
    def interrupt_signal_handler(self, *_):
        """Faengt den CTRL-C Interrupt auf, beendet die anderen Threads und das main Programm"""
        log.critical(f"interrupt signal catched.")
        self.herzschlagmesser_thread_active = False
        self.temp_thread_active = False
        time.sleep(0.5)
        self.__del__()
    
    def on_receive_buzzer_state(self, state):
        """Wenn der buzzer über Thingsboard geaendert wird, wird der Zustand hier geändert"""
        log.info(f"received update for buzzer state: {state}")
        self.buzzer_enabled = state 


    def send_temperature(self, temperature: float):
        """Sende die aktualle Temperatur dem Thingsboard server"""
        log.info(f"Send Temperature: {temperature}°C")
        if temperature:
            self.thingsboard_client.send({self.TEMP_TELEMETRY: temperature})

    def temp_auswertung_thread(self):
        """mit der bestimmten Abtastrate wird der Temperatursensor abgetastet"""
        while self.temp_thread_active:
            temp = self.temperatur_sensor.get_temperature()
            
            self.send_pulse()
            self.send_temperature(temp)
            time.sleep(self.temperatur_sensor.ABTASTRATE)

    
    def on_receive_alarm(self, alarm_state: bool):
        """Sobald der Alarm vom Thingsboard ausgelöst wird, tönt der Buzzer, falls er aktiviert ist"""
        log.warning(f"Alarm state: {alarm_state}")
        
        if alarm_state and self.buzzer_enabled:
            self.buzzer.SOS()
    
    def start_temperatur_auswertung(self):
        """Starte die periodische Auswertung des Temperatursensore sowie die Datenübermittlung an das thingsboard"""
        self.temperatur_sensor = TemperaturSensor()
        temp_thread = Thread(target=self.temp_auswertung_thread)
        temp_thread.start()
        
        self.thingsboard_client.subscribe_to_attribute(self.TEMP_ALARM_ATTR, self.on_receive_alarm)
        self.thingsboard_client.subscribe_to_attribute(self.PULSE_ALARM_ATTR, self.on_receive_alarm)





    def plot_herzschlag(self, value):
        """Lasse bei einem erkannten Puls die LED kurz blinken"""
        # log.debug(f"max: {value}  {(value-10000)//300 * '#'} \r")
        self.alarm_led.blink()

    def send_pulse(self):
        """Sende dem Thingsboard den aktuellen Puls, wenn vorhanden"""
        if self.herzschlag_messer:
            if puls := self.herzschlag_messer.puls:
                telemetry = {self.PULS_TELEMETRY: puls}

                log.info(f"{puls=}")
                self.thingsboard_client.send(telemetry)
        
        
    def show_herzschlag_on_strip(self, current_value: int):
        """Zeige Herzschlag-Verlauf auf dem LED Strip an"""
        self.led_strip.on_receive_herzschlag_value(current_value, self.herzschlag_messer.puls)

        
    # def save_new_herzschlag_value(self, current_value: int):
    #     """Jeder neue Wert wird gespeichert. Wenn der Speicher 10 Werte ueberschreitet 
    #     werden die Daten gebuendelt Thingsboard uebermittelt und den Speicher geloescht."""
    #     current_time = time.time()
    #     self.herzschlagvalue_stack.append([current_time, current_value])
        
    #     if len(self.herzschlagvalue_stack) > 10:
    #         self.send_herzschlagvalue_stack(self.herzschlagvalue_stack)
    #         self.herzschlagvalue_stack.clear()
    
    # def send_herzschlagvalue_stack(self, value_stack: list):
    #     pass
        
    def herzschlag_messer_thread(self):
        """Periodische Abfrage des Herzschlages und erkennen des Maximums"""
        while self.herzschlagmesser_thread_active:
            current_herzschlag_value = self.herzschlag_messer.abtastung()
            self.show_herzschlag_on_strip(current_herzschlag_value)
            # self.save_new_herzschlag_value(current_herzschlag_value)

            time.sleep(self.herzschlag_messer.ABTASTRATE)


    def start_herzschlag_messung(self):
        """Starte die periodische Abtastung des Herzschlagsensor"""
        self.herzschlag_messer = HerzschlagMessung(self.plot_herzschlag)
        herzschlag_thread = Thread(target=self.herzschlag_messer_thread)
        herzschlag_thread.start()
            
            
    def __del__(self):
        """Schalte alle LEDs beim löschen dieses Objektes aus """
        log.info("Clearing LEDs")
        self.alarm_led.off()
        self.led_strip.clear()
        


if __name__ == "__main__":
    artz = Arzt()
    artz.start_temperatur_auswertung()
    artz.start_herzschlag_messung()
    del artz