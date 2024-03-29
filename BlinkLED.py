
import time
import RPi.GPIO as GPIO
from threading import Thread


class LED:
    """stellt die LED KY-034 dar. Diese soll beim Herzschlag kurz blinken"""
    
    def __init__(self) -> None:
        self.setup()
    
    def setup(self):
        """Initialisert die LED, die auf dem GPIO Pin 24 angeschlossen ist"""
        GPIO.setmode(GPIO.BCM)
        
        self.LED_PIN = 24
        GPIO.setup(self.LED_PIN, GPIO.OUT, initial= GPIO.LOW)
    
    
    def blink_thread(self):
        """Thread funktion: Hier kann in einem separaten Thread die LED angelassen, gewartet und ausgeschaltet werden."""
        GPIO.output(self.LED_PIN, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(self.LED_PIN, GPIO.LOW)
        
    def blink(self):
        """Laesst die LED fuer 0.3s blinken. Dafuer wird ein neuer Thread aufgerufen"""
        thread = Thread(target = self.blink_thread)
        thread.start()
        
        
    def off(self):
        """Schalte die LED aus."""
        GPIO.output(self.LED_PIN, GPIO.LOW)
    