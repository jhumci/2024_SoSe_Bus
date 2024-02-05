import time
import board
import digitalio


led_pin = board.GP1      # Replace with the GPIO pin connected to your LED


led = digitalio.DigitalInOut(led_pin)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = not led.value  # Toggle the LED state
    time.sleep(0.2)  # Add a small delay for debouncing
    time.sleep(0.1)