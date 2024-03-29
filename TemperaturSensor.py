# coding=utf-8
# Benötigte Module werden importiert und eingerichtet
import glob
import time
from time import sleep
import RPi.GPIO as GPIO
 
# An dieser Stelle kann die Pause zwischen den einzelnen Messungen eingestellt werden
sleeptime = 1

def setup():
	# Der One-Wire Eingangspin wird deklariert und der integrierte Pull-up-Widerstand aktiviert
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	# Nach Aktivierung des Pull-UP Widerstandes wird gewartet,
	# bis die Kommunikation mit dem DS18B20 Sensor aufgebaut ist
	print ("Warte auf Initialisierung...")
	
	base_dir = '/sys/bus/w1/devices/'
	while True:
		try:
			print("searching for folder")
			device_folder = glob.glob(base_dir + '28*')[0]
			break
		except IndexError:
			sleep(0.5)
			continue
	global device_file
	device_file = device_folder + '/w1_slave'
	
 
# Funktion wird definiert, mit dem der aktuelle Messwert am Sensor ausgelesen werden kann
def TemperaturMessung():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines
 

 
# Die Temperaturauswertung: Beim Raspberry Pi werden erkannte One-Wire Slaves im Ordner
# /sys/bus/w1/devices/ einem eigenen Unterordner zugeordnet. In diesem Ordner befindet sich die Datei w1-slave
# in dem die Daten, die über den One-Wire Bus gesendet wurden gespeichert.
# In dieser Funktion werden diese Daten analysiert und die Temperatur herausgelesen und ausgegeben
def TemperaturAuswertung():
	try:
		lines = TemperaturMessung()
		while lines[0].strip()[-3:] != 'YES':
			time.sleep(0.2)
			lines = TemperaturMessung()
		equals_pos = lines[1].find('t=')
		if equals_pos != -1:
			temp_string = lines[1][equals_pos+2:]
			temp_c = float(temp_string) / 1000.0
			return temp_c
	except:
		return None

# Hauptprogrammschleife
# Die gemessene Temperatur wird in die Konsole ausgegeben - zwischen den einzelnen Messungen
# ist eine Pause, deren Länge mit der Variable "sleeptime" eingestellt werden kann

if __name__ == "__main__":
	try:
		setup()
		TemperaturMessung()
		while True:
			print ("---------------------------------------")
			print ("Temperatur:", TemperaturAuswertung(), "degC")
			time.sleep(sleeptime)
	
	except KeyboardInterrupt:
		GPIO.cleanup()
		