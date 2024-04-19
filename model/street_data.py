from enums.direction import Direction


class StreetData:

    def __init__(self, street_id: int, direction: Direction):
        self.street_id = street_id
        self.direction = direction
        self.min_percentage = 0
        self.max_percentage = 100
