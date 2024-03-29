
### Hardware:

 - Herzschlagsensor
 - AD Wandler
 - 7 Farben LED
 - (1 Farbe LED)
 - Temperatursensor
 - Buzzer


## Thingsboard

### Diagramme: 

 - Temperatur Zeitverlauf
 - Herzschlag Verlauf??

### Alarme:

 - Temperatur zu hoch
 - Puls zu hoch

 ### Schalter:

 - Buzzer-Alarm umschalten



 ## Software

#### Herzschlag:
liest alle 0.01s den Sensor aus, erkennt maximum
bei maximum:
LED blinkt kurz

Bei zu hohen Puls:
andere LED leuchtet
Alarm Attribute auf Thingsboard schicken

gebundelte Packete mit Messwerte an Thingsboard schicken
Puls an Thingsboard schicken

#### Temperatur
liest alle x s den Temperatursensor aus
messwerte an Thingsboard schicken

bei zu hoher Temperatur:
andere LED leuchtet
Alarm Attribute an Thingsboard schicken

#### LED Streifen

zeigt den Verlauf des Herzschlages an
Amplitude als Farbe /Helligkeit

(Amplitude: hoehre Helligkeit, hoher Frequenz: Farbe rot(zu hoch) oder gruen(guter puls))
