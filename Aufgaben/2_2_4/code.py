import board
import analogio
import time
import digitalio

# LED setup
led_pin = board.GP1  # Replace with actual GPIO pin
led = digitalio.DigitalInOut(led_pin)
led.direction = digitalio.Direction.OUTPUT

# Button setup
button_pin = board.GP0  # Replace with actual GPIO pin
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
#button.pull = digitalio.Pull.UP  # Use pull-up resistor

# ADC setup
ldr = analogio.AnalogIn(board.A0)

def adc_to_voltage(adc):
    u_max = 3.3
    u_min = 0.0
    adc_max = 2**16 - 1
    adc_min = 0

    beta_0 = u_min
    beta_1 = (u_max - u_min) / (adc_max - adc_min)
    return beta_0 + beta_1 * adc

def adc_to_e(adc):
    return 15468527.7 / (adc - 1013.94) - 407.92

P_ACT = False
L_MAN = False

PAR_SETPT = 300

prev_button_state = True  # Start with button unpressed
last_press_time = 0  # Time tracking for debounce

# Main loop
while True:
    #print(time.time(), button.value)

    time.sleep(1)

    button_state = button.value  # Read button state (True = not pressed, False = pressed)
    
    current_time = time.monotonic()  # Get the current time in seconds
    
    # Detect a button press event (only on state change)
    if not button_state and prev_button_state:  # Button just pressed
        if current_time - last_press_time > 0.2:  # Debounce (200 ms)
            P_ACT = not P_ACT  # Toggle P_ACT
            last_press_time = current_time  # Update last press time

    prev_button_state = button_state  # Update previous button state

    # Print status
    if P_ACT:
        print("Person anwesend!")
    else:
        print("Niemand da!")

    # Read ADC and convert
    H_ROOM = adc_to_e(ldr.value)
    print("E in Lux", H_ROOM)

    # Control LED
    led.value = (P_ACT and H_ROOM < PAR_SETPT) or L_MAN

    time.sleep(1)  # Short delay to reduce CPU usage