import time
from rpi_ws281x import PixelStrip, Color
import argparse
import random
from collections import deque

# LED strip configuration:
LED_COUNT = 90        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def colorWipe(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def on_receive_herzschlag_value(current_value: int, strip):
    # Skalieren der Zufallszahl von 0-13000 auf 0-255
    skalierte_wert = min(current_value // 51, 255)  # Umrechnung auf den Bereich von 0 bis 255
    print("Skalierte Wert:", skalierte_wert)

    # Erstellen einer Warteschlange mit einer maximalen Länge von 90
    warteschlange = deque(maxlen=90)
    
    # Hinzufügen der skalierten Zufallszahl zur Warteschlange
    for _ in range(90):
        warteschlange.append(skalierte_wert)

    # Aktualisieren der LED-Pixel mit den Helligkeitswerten aus der Warteschlange
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(warteschlange[i], 0, 0))  # Verwende den Helligkeitswert für Rot, andere Farbkomponenten sind 0
    strip.show()

if __name__ == '__main__':
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    try:
        while True:
            print('Updating LED strip with scaled random value.')
            on_receive_herzschlag_value(random.randint(0, 13000), strip)

    except KeyboardInterrupt:
        colorWipe(strip, Color(0, 0, 0), 10)
