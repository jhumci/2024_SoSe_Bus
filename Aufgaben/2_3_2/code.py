import board
import digitalio
import time
from sensor import LDRSensor
from tageslichtschaltung import l_set

# Parameter
PAR_OND  = 100   # Lux: einschalten, wenn Helligkeit darunter faellt
PAR_OFFD = 300   # Lux: ausschalten, wenn Helligkeit darueber steigt
L_MAN    = False

# Hardware initialisieren
sensor = LDRSensor(board.A0, n=10)   # Sensor mit Puffer der Groesse 10

button = digitalio.DigitalInOut(board.GP2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.GP15)
led.direction = digitalio.Direction.OUTPUT

# Startzustand
l_last = False

while True:
    sensor.update()             # neuen Messwert in den Puffer aufnehmen
    h_room = sensor.get_lux()  # geglaetteten Wert abrufen
    p_act  = not button.value

    l_last = l_set(p_act, h_room, PAR_OND, PAR_OFFD, L_MAN, l_last)
    led.value = l_last

    print(f"H_ROOM: {h_room:.1f} Lux | P_ACT: {p_act} | L_SET: {l_last}")
    time.sleep(0.1)
