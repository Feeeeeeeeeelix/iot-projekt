
from rpi_ws281x import PixelStrip

class LedStrip(PixelStrip):
    def __init__(self, num, pin):
        super().__init__(num, pin)

        self.begin()
        
    def setPixelColor(self, n, color):
        return super().setPixelColor(n, color)
    
    
    def show(self):
        return super().show()
