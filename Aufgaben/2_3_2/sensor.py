import analogio, math
from mappings import map_log_log_lin

class LDRSensor:
    """Helligkeitssensor (LDR) mit gleitendem Mittelwert."""

    def __init__(self, pin, n=10):
        self.adc    = analogio.AnalogIn(pin)
        self.n      = n
        self.buffer = [self.adc.value] * n   # Puffer vorbelegen

    def update(self):
        self.buffer.pop(0)
        self.buffer.append(self.adc.value)

    def get_lux(self):
        avg = sum(self.buffer) / self.n
        return map_log_log_lin(avg)