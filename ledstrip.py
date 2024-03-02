
import time
from rpi_ws281x import PixelStrip, Color
from PIL import Image

LED_Anzahl = 45         # Anzahl LEDs
LED_PIN = 18            # GPIO pin
LED_freq = 800000       # LED Frequenz
LED_DMA = 10            # DMA Kanal (wird von der Bibliothek benoetigt)
LED_Helligkeit = 30     # Helligkeit (0-255) bei direkter Ansteuerung über den Pi nur 30!!
LED_invert = False      # kann Farbe invertieren

strip = PixelStrip(LED_Anzahl, LED_PIN, LED_freq, LED_DMA, LED_invert, LED_Helligkeit)
strip.begin()

# Bild auf LED Anzahl skalieren
def Bildskalierung(Bild_Pfad, LED_Anzahl):

    try:
        Bild = Image.open(Bild_Pfad)
        Bild_Verhaeltnis = Bild.width / Bild.height
        new_width = int(Bild_Verhaeltnis * LED_Anzahl)
        new_Bild = Bild.resize((new_width, LED_Anzahl), Image.ANTIALIAS)        # ANTIALIAS für Interpolation (Verschoenerung)
        return new_Bild, new_width                                            
    
    except Exception as error:
        print("Fehler beim Laden des Bildes: ", error)
        return None, None

# Vertikale "Scheibe" des Bildes darstellen
def Bildscheibe(strip, Bild, Scheibe_Position, Scheibe_width = 1):

    for y in range(Bild.height):
        for x in range(Scheibe_Position, Scheibe_Position + Scheibe_width):
            if x < Bild.width:
                Pixel = Bild.getpixel((x, y))

                if y < strip.numPixels():
                    strip.setPixelColor(y, Color(Pixel[0], Pixel[1], Pixel[2]))
    strip.show()

# Berechnung der Aenderungsrate
def Aenderungsrate(new_width):   

    n = 1900                      # Drehzahl in min^-1
    t = 60 / n                    # Zeit pro Umdrehung in Sekunden
    a = t / new_width             # Aenderungsrate berechnen
    return a                      # Aenderungsrate zurückgeben

# Hauptlogik
if _name_ == '_main_':

    try:
        Bild_Pfad = "/home/pi/sui.jpg"                                          # Bildpfad eingeben
        Bild, new_width = Bildskalierung(Bild_Pfad, LED_Anzahl)                 
        Scheibe_width = 1                                                       # Breite "Scheibe" (1 Pixel)
                                                        
        while True:                                                             # Schleife

            for Scheibe_Position in range(0, Bild.width, Scheibe_width):
                Bildscheibe(strip, Bild, Scheibe_Position, Scheibe_width)
                time.sleep(Aenderungsrate(new_width))                           # berechnete Aenderungsrate einfuegen                                

    except KeyboardInterrupt:                                                   # Schleife unterbrechen 

        for i in range(LED_Anzahl):
            strip.setPixelColor(i, Color(0, 0, 0))

        strip.show()