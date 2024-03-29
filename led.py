
import RPi.GPIO as GPIO
import time

class LED:
    def __init__(self) -> None:
        self.setup()
    
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        
        self.LED_PIN = 24
        GPIO.setup(self.LED_PIN, GPIO.OUT, initial= GPIO.LOW)
    
    def blink(self):
        GPIO.output(self.LED_PIN, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(self.LED_PIN, GPIO.LOW)
        
    def off(self):
        GPIO.output(self.LED_PIN, GPIO.LOW)
    