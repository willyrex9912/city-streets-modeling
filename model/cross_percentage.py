from model.street import Street


class CrossPercentage:

    def __init__(self, street_a: Street, street_b: Street, percentage: float):
        self.street_a = street_a
        self.street_b = street_b
        self.time_percentage = percentage
