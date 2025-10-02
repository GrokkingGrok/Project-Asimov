from mesa import Agent

class Enterprise(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, model):
        # Pass the parameters to the parent class.
        super().__init__(model)
        self.inventory = 200000
        self.income = 0.0