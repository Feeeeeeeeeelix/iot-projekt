
import time
import logging
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class HerzschlagMessung:
    ABTASTRATE = 0.01
    
    def __init__(self, maximum_callback, send_callback, strip_callback):
        self.setup()
        self.callback = maximum_callback
        self.send_callback = send_callback
        self.strip_callback = strip_callback
        
        self.value_stack = []
        self.puls = None
    

    def setup(self):
        """Initialisert den Herzschlagsensor Input am AD Wandler am I2C Bus Pin"""
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)

        self.sensor = AnalogIn(ads, ADS.P0)

    def erkenne_maximum(self):
        """Tastet den Sensore alle 10ms ab und erkennt jedes lokale Maximum"""

        currentValue = self.sensor.value

        maximum = currentValue
        maximumTime = time.time()
        valuesUnderMaximum = 0
        searchingForMaximum = True

        minimum = currentValue
        valuesOverMinimum = 0
        
        THRESHHOLD = 2
        THRESSHOLDRATIO = 0.95
        
        while True:
            # Abfrage eines neuen Werts
            currentValue = self.sensor.value
            self.new_value(currentValue)
            log.debug(f"{currentValue:>5} {maximum:>5} {valuesUnderMaximum:>2} {valuesOverMinimum:>2} {searchingForMaximum:>5} {minimum:>5} {(currentValue-10000)//300 * '#'} \r")
            
            if currentValue > maximum:
                # Die werte steigen. der neue Wert wird zum neuen Maximum. 
                maximum = currentValue
                maximumTime = time.time()
                valuesUnderMaximum = 0
            elif currentValue < maximum:
                # Die werte sinken wieder
                valuesUnderMaximum += 1
                
            if valuesUnderMaximum >= THRESHHOLD and searchingForMaximum and currentValue < THRESSHOLDRATIO*maximum:
                # Maximum erkannt
                # nach 2 aufeinanderfolgende sinkende Werte die kleiner als 0.95 des letzten 
                # lokalen Maximums sind, wird das letzte Maximum als solches anerkannt.
                # Zwischen zwei Maxima muss immer ein Minimum liegen, deshalb wird noch ueberprueft, 
                # dass man gerade nach einem Maximum sucht
                self.maximum_erkannt(maximum, maximumTime)
                minimum = currentValue
                valuesUnderMaximum = 0
                searchingForMaximum = False
                valuesOverMinimum = 0
        
                    
            if currentValue < minimum:
                # Sinkende Werte: der aktuelle wird zum neuen Minimum
                minimum = currentValue
                valuesOverMinimum = 0
            elif currentValue > minimum:
                # Steigende Werte nach einem Minimum
                valuesOverMinimum += 1
            
            if valuesOverMinimum >= THRESHHOLD and not searchingForMaximum:
                # minimum erkannt. 
                # Zwischen zwei Minima muss sich ein Maximum befinden
                maximum = currentValue
                valuesOverMinimum = 0
                valuesUnderMaximum = 0
                searchingForMaximum = True
                
            time.sleep(self.ABTASTRATE)

    def maximum_erkannt(self, value: int, time: time):
        """wird aufgerufen, sobald ein Maximum erkannt wurde. value: Wert des Maximum, time: Datum dieses Maximums"""
        log.info(f"MAXIMUM: {value=}--------------------------------------------------------------------- \r")
        
        self.callback(value)
        
        self.berechne_puls
        

    def new_value(self, current_value: int):
        """Bei jeder neune Abstastung wird der aktuelle Wert gespeichert und dem LED Strip uebermittelt."""
        self.save_new_value(current_value)
        
        self.strip_callback(current_value)
        
    def save_new_value(self, current_value: int):
        """Jeder neue Wert wird gespeichert. Wenn der Speicher 10 Werte ueberschreitet 
        werden die Daten gebuendelt Thingsboard uebermittelt und den Speicher geloescht."""
        current_time = time.time()
        self.value_stack.append([current_time, current_value])
        
        if len(self.value_stack) > 10:
            self.send_callback(self.value_stack)
            self.value_stack.clear()
    
    def berechne_puls(time_of_maximum: float):
        pass