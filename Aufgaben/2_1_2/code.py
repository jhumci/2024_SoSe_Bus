import time
import board
import digitalio

button_pin = board.GP0  # GPIO-Pin des Tasters

button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Interner Pull-Up-Widerstand

while True:
    if not button.value:  # Taster gedrueckt (LOW)
        print("Button Pressed!")
    else:
        print("Button Released!")

    time.sleep(0.1)  # Entprellung
