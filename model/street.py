

class Street:

    def __init__(self, street_id: int, start_cross_id: int | None, end_cross_id: int | None):
        self.id = street_id
        self.start_cross_id: int | None = start_cross_id
        self.end_cross_id: int | None = end_cross_id
        self.capacity: int = 0

    