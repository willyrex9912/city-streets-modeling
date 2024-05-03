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
        for key, cross in cross_streets_map.items():
            name = str(key)
            label = "Cross " + name
            data_list: List[StreetData] = cross.get_streets_by_direction(Direction.START)
            if len(data_list) > 0:
                label += "\nOut = [ "
                for data in data_list:
                    label += str(data.street_id) + ":" + str(individual.genes[data.street_id].start_percentage) + "% "
                label += "]"
            dot.node(name, label)
        for key, street in street_map.items():
            name = str(key)
            label = "Street " + name
            if street.start_cross_id is None:
                dot.node('Dummy ' + name, style='invisible')
                dot.edge('Dummy ' + name, str(street.end_cross_id), label=label)
            elif street.end_cross_id is None:
                dot.node('Dummy ' + name, style='invisible')
                dot.edge(str(street.start_cross_id), 'Dummy ' + name, label=label)
            else:
                dot.edge(str(street.start_cross_id), str(street.end_cross_id), label=label)
        caption = f"Total inputs: {individual.total_inputs}\nTotal outputs: {individual.total_outputs}\n"
        caption += f"Total efficiency: {individual.aptitude}%"
        dot.attr(label=caption)
        dot.render('graph', format='png', cleanup=True)
        dot.view()
