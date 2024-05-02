

class RunState:

    def __init__(self, run: bool):
        self.run: bool = run

    def start_run(self):
        self.run = True

    def stop_run(self):
        self.run = False
