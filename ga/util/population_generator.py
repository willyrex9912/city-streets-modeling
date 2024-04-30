from ga.individual import Individual
from typing import Dict, List
from model.street import Street
from model.street_percentage import StreetPercentage
import random


class PopulationGenerator:

    def __init__(self, street_map: Dict[int, Street]):
        self.street_map = street_map
        self.population: List[Individual] = []

    def generate_population(self, population_size: int) -> List[Individual]:
        for _ in range(population_size):
            self.generate_individual()
        # self.print_population()
        return self.population

    def generate_individual(self):
        individual = Individual()
        for street in self.street_map.values():
            street_id = street.id
            start_percentage = random.randint(0, 100)
            end_percentage = random.randint(0, 100)
            individual.genes[street_id] = StreetPercentage(street_id, start_percentage, end_percentage)
        self.population.append(individual)

    def print_population(self):
        for index, individual in enumerate(self.population):
            print(index+1)
            print(individual)
            for gene in individual.genes.values():
                print(vars(gene))
