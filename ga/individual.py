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
        self.min_percentages_efficiency: List[int] = []
        self.max_percentages_efficiency: List[int] = []
        self.aptitude: int = 0

    def calculate_efficiency(self):
        try:
            output_percentage = 100 * self.total_outputs / self.total_inputs
        except ZeroDivisionError:
            output_percentage = 100
        mean_percentages = statistics.mean(self.percentages_efficiency)
        mean_min_percentages = statistics.mean(self.min_percentages_efficiency)
        mean_max_percentages = statistics.mean(self.min_percentages_efficiency)
        self.aptitude = round((output_percentage + mean_percentages + mean_min_percentages + mean_max_percentages) / 4)
