import board
import analogio
import time
import digitalio
from mappings import map_quat

# LED
led_pin = board.GP1      # Replace with the GPIO pin connected to your LED
PAR_SETPT = digitalio.DigitalInOut(led_pin)
PAR_SETPT.direction = digitalio.Direction.OUTPUT

# Button

button_pin = board.GP0  # Replace with the GPIO pin connected to your button
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Use pull-up resistor; change if using pull-down

# Initialisierung des ADC (Analog-Digital Converter)
ldr = analogio.AnalogIn(board.A2)

L_MAN = False
L_SET = 300

# Wiederholung
while True:
    P_ACT = button.value

    # ADC als Dezimalzahl lesen
    H_ROOM = ldr.value
    print("E in Lux", map_quat(H_ROOM))

    PAR_SETPT.value = (P_ACT and map_quat(H_ROOM) < L_SET) or L_MAN)
    # Warten
    time.sleep(1)