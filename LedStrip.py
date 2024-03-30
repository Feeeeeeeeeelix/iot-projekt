import time
import logging
from rpi_ws281x import PixelStrip, Color
from collections import deque
import random


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class LedStrip(PixelStrip):
    LED_COUNT = 90
    LED_PIN = 18    
    
    def __init__(self) -> None:
        super().__init__(self.LED_COUNT, self.LED_PIN)
        self.begin()
        
        self.warteschlange = deque([0]*self.LED_COUNT, maxlen=self.LED_COUNT)

    def on_receive_herzschlag_value(self, current_value: int):
        # Skalieren der Zufallszahl von 0-13000 auf 0-255
        
        skalierte_wert = current_value//69 % 256  # Umrechnung auf den Bereich von 0 bis 255
        log.debug(f"Skalierte Wert: {skalierte_wert}")

        # Erstellen einer Warteschlange mit einer maximalen Länge von 90
        self.warteschlange.appendleft(skalierte_wert)

        for i in range(self.LED_COUNT):
            self.setPixelColor(i, Color(0, int(self.warteschlange[i]*0x5f/0xff),  int(self.warteschlange[i]*0x6a/0xff)))
        self.show()
    
    def clear(self):
        for i in range(self.LED_COUNT):
            self.setPixelColor(i, Color(0,0,0))
        self.show()


if __name__ == '__main__':
    strip = LedStrip()

    try:
        while True:
            strip.on_receive_herzschlag_value(random.randint(0, 13000))
            time.sleep(0.1)

    except KeyboardInterrupt:
        strip.clear()
