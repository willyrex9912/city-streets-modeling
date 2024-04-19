from typing import Dict
from enums.direction import Direction
from model.street_data import StreetData


class CrossStreets:

    def __init__(self, cross_streets_id: int):
        self.id = cross_streets_id
        self.street_map: Dict[int, StreetData] = {}

    def add_street(self, street_id: int, direction: Direction):
        new_street_data = StreetData(street_id, direction)
        self.street_map[street_id] = new_street_data
