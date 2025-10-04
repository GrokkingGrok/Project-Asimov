from mesa import Agent

class RoboFund(Agent):
    """RoboFund hosts Projects provided by Enterprises, and Bondholders decide whether to invest in them."""

    def __init__(self, model):
        # Pass the parameters to the parent class.
        super().__init__(model)