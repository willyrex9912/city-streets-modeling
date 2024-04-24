from typing import Dict
from model.street_percentage import StreetPercentage


class Individual:

    def __init__(self):
        self.genes: Dict[int, StreetPercentage] = {}
        pass
