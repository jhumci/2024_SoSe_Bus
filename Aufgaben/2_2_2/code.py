import time
import board
import digitalio

PAR_HOLD = 5
PAR_WARN = 2
state = "start"

if state == "start":
    btn1 = digitalio.DigitalInOut(board.GP2)   # Taster Unten
    btn1.direction = digitalio.Direction.INPUT
    btn1.pull = digitalio.Pull.UP

    btn2 = digitalio.DigitalInOut(board.GP3)   # Taster Oben
    btn2.direction = digitalio.Direction.INPUT
    btn2.pull = digitalio.Pull.UP

    btn3 = digitalio.DigitalInOut(board.GP4)   # GLT Dauerbetrieb
    btn3.direction = digitalio.Direction.INPUT
    btn3.pull = digitalio.Pull.UP

    led = digitalio.DigitalInOut(board.GP15)
    led.direction = digitalio.Direction.OUTPUT

    dauer_aktiv = False
    btn3_vorher = True

    state = "LED aus"
    print("Erfolgreich gestartet")

while True:
    time.sleep(0.1)
    taster = not btn1.value or not btn2.value

    # Toggle-Erkennung: nur bei fallender Flanke umschalten
    btn3_jetzt = btn3.value
    if not btn3_jetzt and btn3_vorher:
        dauer_aktiv = not dauer_aktiv
        print("GLT Dauerbetrieb:", dauer_aktiv)
    btn3_vorher = btn3_jetzt

    if state == "LED aus":
        if dauer_aktiv:
            state = "Dauerbetrieb"
            led.value = True
        elif taster:
            state = "LED an"

    elif state == "LED an":
        led.value = True
        time_start = time.time()
        state = "LED leuchtet"

    elif state == "LED leuchtet":
        if dauer_aktiv:
            state = "Dauerbetrieb"
        elif taster:
            state = "LED an"
        elif time.time() - time_start > PAR_HOLD:
            state = "LED flackert"

    elif state == "LED flackert":
        for i in range(5):
            led.value = False
            time.sleep(0.1)
            led.value = True
            time.sleep(0.1)
        time_warning = time.time()
        state = "LED leuchtet2"

    elif state == "LED leuchtet2":
        if dauer_aktiv:
            state = "Dauerbetrieb"
        elif taster:
            state = "LED an"
        elif time.time() - time_warning > PAR_WARN:
            state = "LED aus"
            led.value = False

    elif state == "Dauerbetrieb":
        if not dauer_aktiv:
            state = "LED aus"
            led.value = False