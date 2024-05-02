from typing import Dict
from model.street_percentage import StreetPercentage
from typing import List
import statistics


class Individual:

    def __init__(self):
        self.genes: Dict[int, StreetPercentage] = {}
        self.total_inputs: int = 0
        self.total_outputs: int = 0
        self.percentages_efficiency: List[int] = []
        self.aptitude: int = 0

    def calculate_efficiency(self):
        try:
            output_percentage = 100 * self.total_outputs / self.total_inputs
        except ZeroDivisionError:
            output_percentage = 100
        average = statistics.mean(self.percentages_efficiency)
        self.aptitude = round((output_percentage + average) / 2)
