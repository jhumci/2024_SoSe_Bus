import time
import board
import digitalio

# Taster an GP0 (Eingang mit Pull-Up)
button_pin = board.GP0
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# LED an GP1 (Ausgang)
led_pin = board.GP1
led = digitalio.DigitalInOut(led_pin)
led.direction = digitalio.Direction.OUTPUT

last_button_state = True  # Pull-Up: Ruhezustand = True (HIGH)

while True:
    current_button_state = button.value

    # Flanke erkennen: Taster wurde gerade gedrueckt (HIGH -> LOW)
    if last_button_state and not current_button_state:
        led.value = not led.value  # LED-Zustand umschalten
        print("LED: " + ("AN" if led.value else "AUS"))

    last_button_state = current_button_state
    time.sleep(0.1)  # Entprellung
