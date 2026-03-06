import board
import digitalio
import analogio
import time
from mappings import map_lin, map_log_log_lin

# Initialisierung des ADC (Analog-Digital Converter)
ldr = analogio.AnalogIn(board.A0)

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


    read = ldr.value
    print("Beleuchtungsstärke in Lux:", map_log_log_lin(read))


    # Flanke: war nicht gedrückt, jetzt gedrückt
    if last_button and not current:
        toggle_state = not toggle_state
        led.value = toggle_state
        print(f"Toggle: {toggle_state}")

    last_button = current

    time.sleep(0.05)  # Entprellung