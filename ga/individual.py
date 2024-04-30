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

    def print_efficiency(self):
        print("Total inputs: ", self.total_inputs)
        print("Total outputs: ", self.total_outputs)
        output_percentage = 100 * self.total_outputs / self.total_inputs
        print("Efficiency on input and outputs: " + str(output_percentage) + "%")
        average = statistics.mean(self.percentages_efficiency)
        print("Efficiency on percentages: " + str(average) + "%")
        self.aptitude = round((output_percentage + average) / 2)
        print("Total efficiency: " + str(self.aptitude) + "%")
