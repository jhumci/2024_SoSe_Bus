import mappings
import json

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
        
    def prepare_data(self):
        dict_representation = self.__dict__
        dict_representation.pop("measurements")
        dict_representation.pop("name")
        dict_representation.pop("mapping")
        # Vorsicht json.dumps() erstellt einen String, json.dump() schreibt eine Datei!
        json_representation = json.dumps(dict_representation)
        return json_representation.encode("ascii")
    
    def print_data(self):
        print("This " + self.name + "returns data in " + self.unit)

