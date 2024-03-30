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

    def on_receive_herzschlag_value(self, current_value: int, puls:float):
        """Zeige den Herzschlag-Verlauf an. jeder neue Werte wird in einem FIFO Speicher auf dem LED Strip gemapt."""
        puls = puls if puls else 200
        
        # Skalieren des Messwertes von 0-13000 auf 0-255
        skalierte_wert = current_value//69 % 256 
        log.debug(f"Skalierter Wert: {skalierte_wert}")

        self.warteschlange.appendleft(skalierte_wert)

        for i in range(self.LED_COUNT):
            # Zeige den Herzschlag als Helligkeit an. Die Farbe ist Petrol (RGB: 0x005F6A)
            hue = self.warteschlange[i]
            color = Color(0, int(hue*0x5a/0xFF),int(hue*0x6a/0xff))
            self.setPixelColor(i, color)
        # log.info(f"{color=}, {hue=}, {puls=}")
        self.show()
    
    def clear(self):
        """Schalte alle LEDs aus"""
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
