from ga.individual import Individual
from typing import Dict
from model.cross_streets import CrossStreets
from enums.direction import Direction
import random


class IndividualGenerator:

    def __init__(self, cross_streets_map: Dict[int, CrossStreets]):
        self.cross_streets_map = cross_streets_map

    def generate_individual(self):
        individual = Individual()
        for cross in self.cross_streets_map.values():
            for street in cross.street_map.values():
                street.percentage = self.generate_percentage()
        self.print_cross_info()

    def generate_percentage(self) -> int:
        rand_percentage = random.randint(0, 100)
        return rand_percentage

    def print_cross_info(self):
        for cross in self.cross_streets_map.values():
            inputs = cross.get_streets_by_direction(Direction.END)
            outputs = cross.get_streets_by_direction(Direction.START)
            print("\nCross:")
            print(cross.id)
            print("Inputs:")
            for i in inputs:
                print(vars(i))
            print("Outputs:")
            for o in outputs:
                print(vars(o))
