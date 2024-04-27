from ga.util.population_generator import PopulationGenerator
from typing import List, Dict
from ga.individual import Individual
from model.cross_streets import CrossStreets
from model.street import Street
from enums.direction import Direction


class SolutionGenerator:

    def __init__(self, street_map: Dict[int, Street], population_size:int, cross_streets_map: Dict[int, CrossStreets]):
        self.population_generator = PopulationGenerator(street_map)
        self.population_size = population_size
        self.cross_streets_map = cross_streets_map
        self.street_map = street_map
        self.generations: int = 0
        self.temp_total_inputs: int = 0
        self.temp_total_outputs: int = 0

    def start(self):
        population = self.population_generator.generate_population(self.population_size)
        self.generations += 1
        self.aptitude_function(population)

    def aptitude_function(self, population: List[Individual]) -> int:
        self.calculate_all_cross_percentages(population[0])
        print("FINISHED")
        for index, individual in enumerate(population):
            print(index+1)
            print(individual)
            for gene in individual.genes.values():
                print(vars(gene))
            print("Total inputs: ", self.temp_total_inputs)
            print("Total outputs: ", self.temp_total_outputs)
        return 1

    def calculate_all_cross_percentages(self, individual: Individual):
        for cross in self.cross_streets_map.values():
            if not cross.evaluated:
                self.calculate_cross_percentages(cross.id, individual)
        for cross in self.cross_streets_map.values():
            cross.evaluated = False

    def calculate_cross_percentages(self, cross_id: int, individual: Individual):
        cross: CrossStreets = self.cross_streets_map[cross_id]
        if cross.evaluated:
            return
        total_number = 0
        input_streets = cross.get_streets_by_direction(Direction.END)
        output_streets = cross.get_streets_by_direction(Direction.START)
        for street in input_streets:
            main_street = self.street_map[street.street_id]
            if main_street.start_cross_id is None:
                gen = individual.genes[main_street.id]
                gen.start_number = main_street.capacity
                gen.end_number = main_street.capacity
                self.temp_total_inputs += gen.end_number
                end_number = gen.end_number
                total_number += end_number * 1
            else:
                gen = individual.genes[main_street.id]
                start_number = gen.start_number
                if start_number is None:
                    self.calculate_cross_percentages(main_street.start_cross_id, individual)
                    start_number = gen.start_number
                    total_number += round(start_number * (gen.end_percentage/100))
                    gen.end_number = total_number
                else:
                    total_number += round(start_number * (gen.end_percentage/100))
                    gen.end_number = total_number
        for street in output_streets:
            main_street = self.street_map[street.street_id]
            gen = individual.genes[main_street.id]
            gen.start_number = round(total_number * (gen.start_percentage/100))
            if main_street.end_cross_id is None:
                self.temp_total_outputs += gen.start_number
        cross.evaluated = True
