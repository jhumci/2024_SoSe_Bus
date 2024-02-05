import mappings

class Sensor:
    def __init__(self, name, unit, selected_mapping):
        self.name = name
        self.unit = unit
        self.last_measurement = None
        self.measurements = []
        self.mapping = selected_mapping

    def do_measurement(self, ldr):
        self.last_measurement = ldr.value
        self.last_measurement = self.mapping(self.last_measurement)

        if len(self.measurements) > 10:
            self.measurements.pop(0)
        self.measurements.append(self.last_measurement)

    def calc_mean(self, n = 10):
        if len(self.measurements) < n:
            return sum(self.measurements[-n:]) / n
        else:
            return sum(self.measurements) / len(self.measurements)
        

            
    def print_data(self):
        print("This " + self.name + "returns data in " + self.unit)
