import time
import board
import digitalio


led_pin = board.GP1      # Replace with the GPIO pin connected to your LED


led = digitalio.DigitalInOut(led_pin)
led.direction = digitalio.Direction.OUTPUT


button_pin = board.GP0  # Replace with the GPIO pin connected to your button

button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Use pull-up resistor; change if using pull-down

while True:
    if not button.value:  # Button is pressed (LOW)
        print("Button Pressed!")
        led.value = not led.value  # Toggle the LED state
    else:
        print("Button Released!")
    
    time.sleep(0.1)  # Add a small delay to debounce the button
