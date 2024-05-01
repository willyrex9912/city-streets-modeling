

class StreetPercentage:

    def __init__(self, street_id: int, start_percentage: int, end_percentage: int):
        self.street_id = street_id
        self.start_percentage: int = start_percentage
        self.end_percentage: int = end_percentage
        self.start_number: int | None = None
        self.end_number: int | None = None

    def copy(self):
        return StreetPercentage(self.street_id, self.start_percentage, self.end_percentage)