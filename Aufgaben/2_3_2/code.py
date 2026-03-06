import board
import digitalio
import time
from tageslichtschaltung import l_set
from sensor import LDRSensor

PAR_OND  = 100   # Lux: einschalten, wenn dunkler
PAR_OFFD = 300   # Lux: ausschalten, wenn heller
L_MAN    = False

l_last = False   # Startzustand

# Initialisierung des ADC (Analog-Digital Converter)
sensor = LDRSensor(board.A0, n=10)   # Objekt erstellen

# LED
led = digitalio.DigitalInOut(board.GP15)
led.direction = digitalio.Direction.OUTPUT

# Taster mit internem Pull-Up
button = digitalio.DigitalInOut(board.GP14)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

toggle_state = False
last_button = True  # Pull-Up: nicht gedrückt = True

while True:
    current = button.value  # False = gedrückt (Pull-Up)
    sensor.update()
    h_room = sensor.get_lux()


    # Flanke: war nicht gedrückt, jetzt gedrückt
    if last_button and not current:
        toggle_state = not toggle_state
        led.value = toggle_state
        print(f"Toggle: {toggle_state}")

    last_button = current
    p_act  = last_button
    l_last = l_set(p_act, h_room, PAR_OND, PAR_OFFD, L_MAN, l_last)
    led.value = l_last

    print(f"H_ROOM: {h_room:.1f} Lux | P_ACT: {p_act} | L_SET: {l_last}")

    time.sleep(0.05)  # Entprellung