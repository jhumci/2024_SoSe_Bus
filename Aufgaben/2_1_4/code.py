import pwmio
import board
import time
import digitalio

pwm = pwmio.PWMOut(board.GP1)  # output on LED pin with default of 500Hz
button_pin = board.GP0  # Replace with the GPIO pin connected to your button

button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Use pull-up resistor; change if using pull-down

while True:
    if not button.value:  # Button is pressed (LOW)
        print("Button Pressed!")
        pwm.duty_cycle = 65535
        time.sleep(1)
        for cycle in range(65534, 0, -1):  # Cycles through the PWM range backwards from 65534 to 0
            pwm.duty_cycle = cycle  # Cycles the LED pin duty cycle through the range of values
            time.sleep(0.0005)
