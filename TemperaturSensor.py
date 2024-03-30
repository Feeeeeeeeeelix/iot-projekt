
import glob
import time
import logging
from threading import Thread
import RPi.GPIO as GPIO

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

 
class TemperaturSensor:
    """ stellt den Temperatursensor KY001 dar.
    teilweise uebernommen und angepasst von: https://sensorkit.joy-it.net/de/sensors/ky-001"""
    
    MAX_TEMPERATURE_THRESHHOLD = 26
    ABTASTRATE = 1
    
    def __init__(self, alarm_callback) -> None:
        self.setup()

        self.is_critical = False
        self.alarm_callback = alarm_callback
    
        
    def setup(self):
        """Initialisiere den Temperatursensor auf dem GPIO PIN 4"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        log.info("Warte auf Initialisierung...")
        
        base_dir = '/sys/bus/w1/devices/'
        while True:
            try:
                log.debug("Suche nach Ordner")
                device_folder = glob.glob(base_dir + '28*')[0]
                break
            except IndexError:
                time.sleep(0.5)
                continue
            
        self.device_file = device_folder + '/w1_slave'
    
 
    def read_file(self) -> list:
        """Der Temperatursensor wird als One-Wire Slaves im Ordner /sys/bus/w1/devices/ 
        als Datei erfasst, in der die gespeicherten Messwerte stehen"""
        with open(self.device_file, "r") as file:
            lines = file.readlines()
        return lines
 
    def get_temperature(self) -> float:
        """Gebe die aktuell gemessene Temperatur in °C zurueck."""
        
        try:
            lines = self.read_file()
            log.debug(f"{lines=}")
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                log.error(f"Error while reading temperature from file {lines=}")
                lines = self.read_file()
                
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                
                # self.check_temperature(temp_c)
                return temp_c
        except Exception:
            return None
    
    def check_temperature(self, temperature: float):
        if temperature > self.MAX_TEMPERATURE_THRESHHOLD:
            self.is_critical = True
            self.alarm_callback(temperature)

    
    def __del__(self):
        GPIO.cleanup()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    
    temp_sensor = TemperaturSensor()
    try:
        for i in range(20):
            log.info(temp_sensor.get_temperature())
    except KeyboardInterrupt:
        exit()