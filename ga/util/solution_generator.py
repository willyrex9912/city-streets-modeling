from ga.util.population_generator import PopulationGenerator
from typing import List, Dict
from ga.individual import Individual
from model.cross_streets import CrossStreets
from model.street import Street
from enums.direction import Direction
from ga.enums.termination_criteria import TerminationCriteria
from util.grapher import Grapher
import random


class SolutionGenerator:

    def __init__(self, street_map: Dict[int, Street], population_size: int, cross_streets_map: Dict[int, CrossStreets],
                 termination_criteria: TerminationCriteria, termination_value: int, mutation_size: int,
                 mutation_generations: int):
        self.population_generator = PopulationGenerator(street_map)
        self.population_size = population_size
        self.cross_streets_map = cross_streets_map
        self.street_map = street_map
        self.generation: int = 0
        self.population: List[Individual] = []
        self.best_individual: Individual | None = None
        self.termination_criteria: TerminationCriteria = termination_criteria
        self.termination_value: int = termination_value
        self.mutation_size: int = mutation_size
        self.mutation_generations: int = mutation_generations

    def start(self):
        self.population = self.population_generator.generate_population(self.population_size)
        self.generation += 1
        print(f"Generation {self.generation}")
        self.work_generation(self.population)
        while self.objetive_function() is False:
            self.generation += 1
            print(f"Generation {self.generation}")
            self.work_generation(self.generate_population_by_roulette())
        print("BEST INDIVIDUAL FOUND:")
        self.best_individual.print_efficiency()
        Grapher.graph(self.cross_streets_map, self.street_map, self.best_individual)

    def objetive_function(self) -> bool:
        for individual in self.population:
            if self.best_individual is None:
                self.best_individual = individual
            else:
                if individual.aptitude > self.best_individual.aptitude:
                    self.best_individual = individual
        if self.termination_criteria == TerminationCriteria.GENERATION_NUMBER:
            return self.termination_value == self.generation
        elif self.termination_criteria == TerminationCriteria.EFFICIENCY_PERCENTAGE:
            if self.termination_value <= self.best_individual.aptitude:
                return True
        return False

    def work_generation(self, population: List[Individual]):
        self.apply_mutation()
        for individual in population:
            self.calculate_all_cross_percentages(individual)
        for index, individual in enumerate(population):
            print(index+1)
            print(individual)
            individual.print_efficiency()

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
                individual.total_inputs += gen.end_number
                end_number = gen.end_number
                total_number += end_number * 1
            else:
                gen = individual.genes[main_street.id]
                start_number = gen.start_number
                if start_number is None:
                    self.calculate_cross_percentages(main_street.start_cross_id, individual)
                    start_number = gen.start_number
                max_number = round(main_street.capacity * (gen.end_percentage / 100))
                if start_number <= max_number:
                    gen.end_number = start_number
                    total_number += start_number
                else:
                    gen.end_number = max_number
                    total_number += max_number
        for street in output_streets:
            main_street = self.street_map[street.street_id]
            gen = individual.genes[main_street.id]
            max_number = round(main_street.capacity * (gen.start_percentage / 100))
            gen.start_number = round(total_number * (gen.start_percentage/100))
            if gen.start_number > max_number:
                gen.start_number = max_number
            if main_street.end_cross_id is None:
                individual.total_outputs += gen.start_number
        cross.evaluated = True
        # Input percentage save to verify after
        input_percentage = 0
        for street in input_streets:
            input_percentage += individual.genes[street.street_id].end_percentage
        output_percentage = 0
        for street in input_streets:
            output_percentage += individual.genes[street.street_id].start_percentage
        if input_percentage <= 100 and output_percentage <= 100:
            individual.percentages_efficiency.append(100)
        elif input_percentage <= 100 or output_percentage <= 100:
            individual.percentages_efficiency.append(50)
        else:
            individual.percentages_efficiency.append(0)

    def generate_population_by_roulette(self) -> List[Individual]:
        population = []
        while len(population) < self.population_size:
            first = self.select_by_roulette()
            second = self.select_by_roulette()
            population.extend(self.cross_individuals(first, second))
        self.population = population
        return population

    @staticmethod
    def cross_individuals(first: Individual, second: Individual) -> List[Individual]:
        keys = list(first.genes.keys())
        middle = len(keys) // 2
        new_1 = {key: first.genes[key].copy() for key in keys[:middle]}
        new_1.update({key: second.genes[key].copy() for key in keys[middle:]})
        new_2 = {key: second.genes[key].copy() for key in keys[:middle]}
        new_2.update({key: first.genes[key].copy() for key in keys[middle:]})

        new_individual_1 = Individual()
        new_individual_1.genes = new_1
        new_individual_2 = Individual()
        new_individual_2.genes = new_2
        return [new_individual_1, new_individual_2]

    def select_by_roulette(self) -> Individual:
        s = sum(individual.aptitude for individual in self.population)
        a = random.randint(0, s)
        value = 0
        for individual in self.population:
            value = value + individual.aptitude
            if value >= a:
                return individual

    def apply_mutation(self):
        if self.generation % self.mutation_generations == 0:
            for i in range(self.mutation_size):
                self.mutate(random.choice(self.population))

    @staticmethod
    def mutate(individual: Individual):
        key: int = random.choice(list(individual.genes.keys()))
        individual.genes[key].start_percentage = random.randint(0, 100)
        individual.genes[key].end_percentage = random.randint(0, 100)
