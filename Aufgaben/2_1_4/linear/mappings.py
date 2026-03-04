import board
import analogio
import time

from mappings import map_lin

# Initialisierung des ADC (Analog-Digital Converter)
ldr = analogio.AnalogIn(board.A0)

# Wiederholung
while True:
    # ADC als Dezimalzahl lesen
    read = ldr.value
    # Ausgabe in der Kommandozeile/Shell
    print("ADC:", read)
    print("Spannunng in V:", map_lin(read))
    print("\n") # neue Zeile
    # Warten
    time.sleep(1)