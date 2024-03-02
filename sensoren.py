import os

# Pfad zur Datei, die die Temperaturdaten enthält
device_file = '/sys/bus/w1/devices/28-XXXXXXXXXXXX/w1_slave'  # Ersetze XXXXXXXX durch die entsprechende Seriennummer deines Sensors

def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        pass
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

# Hauptprogramm
try:
    while True:
        print("Temperatur:", read_temp(), "°C")
except KeyboardInterrupt:
    print("\nProgramm wurde beendet.")

