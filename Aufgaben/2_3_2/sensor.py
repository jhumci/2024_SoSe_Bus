import analogio
import math

LN10   = math.log(10)
BETA_1 = -2.3332
BETA_0 = 11.9614

def map_log_log_lin(z):
    """Rechnet ADC-Rohwert in Beleuchtungsstaerke (Lux) um."""
    if z < 1:
        z = 1
    log10_z = math.log(z) / LN10
    log10_E = BETA_1 * log10_z + BETA_0
    return math.exp(log10_E * LN10)


class LDRSensor:
    """
    Helligkeitssensor (LDR) mit gleitendem Mittelwert.

    Attribute:
        adc    – AnalogIn-Objekt fuer den ADC-Pin
        n      – Anzahl der Messwerte im Puffer
        buffer – Liste der letzten n ADC-Rohwerte
    """

    def __init__(self, pin, n=10):
        """
        Erstellt einen neuen LDR-Sensor.

        pin: CircuitPython-Pin (z.B. board.A0)
        n:   Puffergroesse (Anzahl gemittelter Messwerte)
        """
        self.adc    = analogio.AnalogIn(pin)
        self.n      = n
        self.buffer = [self.adc.value] * n   # Puffer mit aktuellem Wert fuellen

    def update(self):
        """Liest einen neuen ADC-Wert und fuegt ihn dem Puffer hinzu."""
        self.buffer.pop(0)                   # aeltesten Wert entfernen
        self.buffer.append(self.adc.value)   # neuen Wert hinzufuegen

    def get_lux(self):
        """Gibt den geglaetteten Helligkeitswert in Lux zurueck."""
        avg = sum(self.buffer) / self.n
        return map_log_log_lin(avg)
