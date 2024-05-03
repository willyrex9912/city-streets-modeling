from typing import Dict
from model.cross_streets import CrossStreets
from model.street import Street
from ga.individual import Individual
from graphviz import Digraph
from ga.enums.termination_criteria import TerminationCriteria


class Grapher:

    @staticmethod
    def graph(cross_streets_map: Dict[int, CrossStreets], street_map: Dict[int, Street], individual: Individual | None):
        dot = Digraph()
        dot.attr(rankdir='LR')
        for key in cross_streets_map.keys():
            name = str(key)
            label = "Cross " + name
            dot.node(name, label)
        for key, street in street_map.items():
            name = str(key)
            label = "Street " + name
            if street.start_cross_id is None:
                dot.node('Dummy ' + name, style='invisible')
                label += f"\nPercentage: 100%"
                label += f"\nTotal: {street.capacity}"
                dot.edge('Dummy ' + name, str(street.end_cross_id), label=label)
            elif street.end_cross_id is None:
                dot.node('Dummy ' + name, style='invisible')
                label += f"\nPercentage: {individual.genes[street.id].start_percentage}%"
                label += f"\nTotal: {individual.genes[street.id].start_number}"
                dot.edge(str(street.start_cross_id), 'Dummy ' + name, label=label)
            else:
                label += f"\nPercentage: {individual.genes[street.id].start_percentage}%"
                label += f"\nTotal: {individual.genes[street.id].start_number}"
                dot.edge(str(street.start_cross_id), str(street.end_cross_id), label=label)
        caption = f"Total inputs: {individual.total_inputs}\nTotal outputs: {individual.total_outputs}\n"
        caption += f"Total efficiency: {individual.aptitude}%"
        dot.attr(label=caption)
        dot.render('graph', format='png', cleanup=True)
        dot.view()

    @staticmethod
    def pre_graph(cross_streets_map: Dict[int, CrossStreets], street_map: Dict[int, Street], population_size: int,
                  mutation_size: int, mutation_generations: int, termination_criteria: TerminationCriteria,
                  termination_value: int):
        dot = Digraph()
        dot.attr(rankdir='LR')
        for key in cross_streets_map.keys():
            name = str(key)
            label = "Cross " + name
            dot.node(name, label)
        for key, street in street_map.items():
            name = str(key)
            label = "Street " + name
            if street.start_cross_id is None:
                dot.node('Dummy ' + name, style='invisible')
                label += f"\nCapacity: {street.capacity}"
                dot.edge('Dummy ' + name, str(street.end_cross_id), label=label)
            elif street.end_cross_id is None:
                dot.node('Dummy ' + name, style='invisible')
                label += f"\nCapacity: {street.capacity}"
                label += f"\nMin: {cross_streets_map[street.start_cross_id].street_map[street.id].min_percentage}%"
                dot.edge(str(street.start_cross_id), 'Dummy ' + name, label=label)
            else:
                label += f"\nCapacity: {street.capacity}"
                label += f"\nMin: {cross_streets_map[street.start_cross_id].street_map[street.id].min_percentage}%"
                dot.edge(str(street.start_cross_id), str(street.end_cross_id), label=label)
        caption = f"Population size: {population_size}\n"
        caption += f"Mutation: {mutation_size} mutations every {mutation_generations} generations\n"
        if termination_criteria == TerminationCriteria.GENERATION_NUMBER:
            caption += f"Termination criteria: Generation number ({termination_value})\n"
        if termination_criteria == TerminationCriteria.EFFICIENCY_PERCENTAGE:
            caption += f"Termination criteria: Efficiency percentage ({termination_value}%)\n"
        dot.attr(label=caption)
        dot.render('pre_graph', format='png', cleanup=True)
        dot.view()
