from typing import Dict
from typing import List
from model.cross_streets import CrossStreets
from model.street import Street
from ga.individual import Individual
from graphviz import Digraph
from enums.direction import Direction
from model.street_data import StreetData


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
                label += f"\nMin: {cross_streets_map[street.start_cross_id].street_map[street.id].min_percentage}%"
                dot.edge(str(street.start_cross_id), 'Dummy ' + name, label=label)
            else:
                label += f"\nPercentage: {individual.genes[street.id].start_percentage}%"
                label += f"\nTotal: {individual.genes[street.id].start_number}"
                label += f"\nMin: {cross_streets_map[street.start_cross_id].street_map[street.id].min_percentage}%"
                dot.edge(str(street.start_cross_id), str(street.end_cross_id), label=label)
        caption = f"Total inputs: {individual.total_inputs}\nTotal outputs: {individual.total_outputs}\n"
        caption += f"Total efficiency: {individual.aptitude}%"
        dot.attr(label=caption)
        dot.render('graph', format='png', cleanup=True)
        dot.view()
