
import time
import curses
import logging
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

logging.basicConfig(
    format = "%(asctime)s - %(levelname)s - %(message)s",
    level = logging.DEBUG,
)

class HerzschlagMessung:
    def __init__(self, maximum_callback, send_callback):
        
        self.setup()
        self.callback = maximum_callback
        self.send_callback = send_callback
        
        self.value_stack = []

    def setup(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)

        self.chan0 = AnalogIn(ads, ADS.P0)
        # screen = curses.initscr()

    def erkenne_maximum(self):

        currentValue = self.chan0.value

        maximum = currentValue
        maximumTime = time.time()
        valuesUnderMaximum = 0
        searchingForMaximum = True

        minimum = currentValue
        valuesOverMinimum = 0
        
        THRESHHOLD = 2
        THRESSHOLDRATIO = 0.95
        try:
            while True:
                currentValue = self.chan0.value
                self.save_new_value(currentValue)
                logging.debug(f"{currentValue:>5} {maximum:>5} {valuesUnderMaximum:>2} {valuesOverMinimum:>2} {searchingForMaximum:>5} {minimum:>5} {(currentValue-10000)//300 * '#'} \r")
                
                if currentValue > maximum:
                    maximum = currentValue
                    maximumTime = time.time()
                    valuesUnderMaximum = 0
                elif currentValue < maximum:
                    valuesUnderMaximum += 1
                    
                if valuesUnderMaximum >= THRESHHOLD and searchingForMaximum and currentValue < THRESSHOLDRATIO*maximum:
                    # maximum erkannt
                    self.maximum_erkannt(maximum, maximumTime)
                    minimum = currentValue
                    valuesUnderMaximum = 0
                    searchingForMaximum = False
                    valuesOverMinimum = 0
            
                        
                if currentValue < minimum:
                    minimum = currentValue
                    valuesOverMinimum = 0
                elif currentValue > minimum:
                    valuesOverMinimum += 1
                
                if valuesOverMinimum >= THRESHHOLD and not searchingForMaximum:
                    # minimum erkannt
                    # logging.debug("minimum erkannt\r")
                    maximum = currentValue
                    valuesOverMinimum = 0
                    valuesUnderMaximum = 0
                    searchingForMaximum = True
                    
                time.sleep(0.01)
                
                
        except KeyboardInterrupt:
            pass


    def maximum_erkannt(self, value: int, time: time):
        self.callback(value)#{"value": value, "time": time})
        logging.info(f"MAXIMUM: {value=}--------------------------------------------------------------------- \r")

    def save_new_value(self, current_value: int):
        current_time = time.time()
        # self.value_stack[current_time] = current_value
        self.value_stack.append([current_time, current_value])
        
        if len(self.value_stack) > 10:
            self.send_callback(self.value_stack)
            self.value_stack.clear()
        
    
    def plot(self):
        while True:
            
            bar_len = self.chan0.value//300 
            
            logging.info("#"*bar_len, "\r")
            
            # screen.clear()
            # screen.addstr(0, 0,  "#" * bar_len)
            # screen.refresh()
            
            time.sleep(0.01)

def lel(a):
    print(a)
    print()

if __name__ == "__main__":
    h = HerzschlagMessung(lel)
    h.erkenne_maximum()
    
    