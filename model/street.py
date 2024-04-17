from model.street_crossing import StreetCrossing


class Street:

    def __init__(self):
        self.start: StreetCrossing = None
        self.end: StreetCrossing = None
        self.capacity: int = 0

    