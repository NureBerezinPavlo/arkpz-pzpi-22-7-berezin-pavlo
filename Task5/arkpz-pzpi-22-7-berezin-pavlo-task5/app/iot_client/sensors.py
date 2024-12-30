import random
from datetime import datetime
from .settings import SETTINGS, UNIT_SYSTEMS

class SensorSimulator:
    def __init__(self):
        self.temperature = 25.0
        self.humidity = 50.0
        self.weight = 0.0
        self.current_floor = 1
        self.is_power_on = True
        self.is_moving = False
        self.is_stuck = False
        self.tempetature_min = -0.5
        self.temperature_max = 0.5
        self.humidity_min = -1.0
        self.humidity_max = 1.0

    def update_simulation_params(self, tempetature_min, temperature_max, 
                                 humidity_min, humidity_max, weight):
        """Оновлення параметрів симуляції."""
        self.tempetature_min = tempetature_min
        self.temperature_max = temperature_max
        self.humidity_min = humidity_min
        self.humidity_max = humidity_max
        self.weight = weight

    def generate_data(self):
        """Генерує випадкові дані для сенсорів"""
        unit_system = UNIT_SYSTEMS[SETTINGS['unit_system']]
        #date_format = SETTINGS['date_format']
        
        if self.is_power_on:
            self.temperature += random.uniform(self.tempetature_min, self.temperature_max)
            self.humidity += random.uniform(self.humidity_min, self.humidity_max)
            self.humidity = min(self.humidity, 100)

            if self.is_moving and not self.is_stuck:
                self.current_floor += 1 if random.random() > 0.5 else -1
                self.current_floor = max(1, self.current_floor)

            return {
                "temperature": round(self.temperature, 2),
                "humidity": round(self.humidity, 2),
                "weight": round(self.weight, 2),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "current_floor": self.current_floor,
                "is_moving": self.is_moving,
                "is_power_on": self.is_power_on,
                "is_stuck": self.is_stuck
            }
        else:
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_stuck": self.is_moving,
                "is_power_on": self.is_power_on,
                "is_moving": False
            }