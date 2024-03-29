
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
    
    THRESHHOLD = 2
    THRESSHOLDRATIO = 0.95
    
    def __init__(self, maximum_callback):
        self.setup_sensor()
        self.callback = maximum_callback
        
        self.value_stack = []
        self.puls = None
    
        currentValue = self.sensor.value

        self.current_maximum = currentValue
        self.current_maximum_time = time.time()
        self.values_under_minimum = 0
        self.searching_for_maximum = True

        self.current_minimum = currentValue
        self.values_over_minimum = 0


    def setup_sensor(self):
        """Initialisert den Herzschlagsensor Input am AD Wandler am I2C Bus Pin"""
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)

        self.sensor = AnalogIn(ads, ADS.P0)

    def erkenne_maximum(self, current_value):
        """Erkennt jedes lokale Maximum"""

        if current_value > self.current_maximum:
            # Die werte steigen. der neue Wert wird zum neuen Maximum. 
            self.current_maximum = current_value
            self.current_maximum_time = time.time()
            self.values_under_minimum = 0
        elif current_value < self.current_maximum:
            # Die werte sinken wieder
            self.values_under_minimum += 1
            
        if self.values_under_minimum >= self.THRESHHOLD and self.searching_for_maximum and current_value < self.THRESSHOLDRATIO*self.current_maximum:
            # Maximum erkannt
            # nach 2 aufeinanderfolgende sinkende Werte die kleiner als 0.95 des letzten 
            # lokalen Maximums sind, wird das letzte Maximum als solches anerkannt.
            # Zwischen zwei Maxima muss immer ein Minimum liegen, deshalb wird noch ueberprueft, 
            # dass man gerade nach einem Maximum sucht
            self.maximum_erkannt(self.current_maximum, self.current_maximum_time)
            self.current_minimum = current_value
            self.values_under_minimum = 0
            self.searching_for_maximum = False
            self.values_over_minimum = 0
    
                
        if current_value < self.current_minimum:
            # Sinkende Werte: der aktuelle wird zum neuen Minimum
            self.current_minimum = current_value
            self.values_over_minimum = 0
        elif current_value > self.current_minimum:
            # Steigende Werte nach einem Minimum
            self.values_over_minimum += 1
        
        if self.values_over_minimum >= self.THRESHHOLD and not self.searching_for_maximum:
            # minimum erkannt. 
            # Zwischen zwei Minima muss sich ein Maximum befinden
            self.current_maximum = current_value
            self.values_over_minimum = 0
            self.values_under_minimum = 0
            self.searching_for_maximum = True
            

    def abtastung(self):
        current_value = self.sensor.value
        
        self.erkenne_maximum(current_value)
        
        # log.debug(f"{current_value:>5} {self.curretn_maximum:>5} {self.values_under_minimum:>2} {self.valuesOverMinimum:>2} {self.searchingForMaximum:>5} {self.minimum:>5} {(current_value-10000)//300 * '#'} \r")
        return current_value
    
    
    def maximum_erkannt(self, value: int, time: time):
        """wird aufgerufen, sobald ein Maximum erkannt wurde. value: Wert des Maximum, time: Datum dieses Maximums"""
        log.debug(f"MAXIMUM: {value=}--------------------------------------------------------------------- \r")
        
        self.callback(value)
        
        self.berechne_puls(time)
        
    def berechne_puls(self, time_of_maximum: float):
        pass