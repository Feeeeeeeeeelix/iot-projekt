
import time
import logging
from threading import Thread
import RPi.GPIO as GPIO

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class Buzzer:
    def __init__(self):
  
        self.buzzer_PIN = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_PIN, GPIO.OUT, initial= GPIO.LOW)
        
        self.is_buzzering = False

    def SOS(self):
        if not self.is_buzzering:
            log.warning(f"Buzzer buzzering...")
            sos_thread = Thread(target=self._sos_thread)
            sos_thread.start()
    
    def _sos_thread(self):
        self.is_buzzering = True
        self._kurz_zeichen(3)
        self._lang_zeichen(3)
        self._kurz_zeichen(3)
        self.is_buzzering = False
        
    def _kurz_zeichen(self, anzahl_der_wiederholung):
        for i in range (anzahl_der_wiederholung):
            log.debug("kurz")
            GPIO.output(self.buzzer_PIN,GPIO.HIGH)   #Buzzer wird eingeschaltet
            time.sleep(0.1)                     #Wartemodus für 0.1 Sekunden
            GPIO.output(self.buzzer_PIN,GPIO.LOW)    #Buzzer wird ausgeschaltet
            time.sleep(0.1)
        self._pause(1)

    def _lang_zeichen(self, anzahl_der_wiederholung):
        for i in range (anzahl_der_wiederholung):
            log.debug("lang")
            GPIO.output(self.buzzer_PIN,GPIO.HIGH)   #Buzzer wird eingeschaltet
            time.sleep(0.3)                     #Wartemodus für 0.3 Sekunden
            GPIO.output(self.buzzer_PIN,GPIO.LOW)    #Buzzer wird ausgeschaltet
            time.sleep(0.1)
        self._pause(1) 
        
    def _pause(self, pause_in_sekunde):
        for i in range (pause_in_sekunde):
            log.debug("pause")
            GPIO.output(self.buzzer_PIN,GPIO.LOW)    #Buzzer wird ausgeschaltet
            time.sleep(pause_in_sekunde) 

    def __del__(self):
        log.info("deleting buzzer")
        GPIO.output(self.buzzer_PIN, GPIO.LOW)
        GPIO.cleanup()

    
 
if __name__ == "__main__":
    logging.basicConfig(
        format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level = logging.DEBUG,
    )
    
    b = Buzzer()
    
    try:
    # while True:
        b.SOS()
    except KeyboardInterrupt:
        del b