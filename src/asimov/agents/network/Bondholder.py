
# Standard library imports
from typing import Optional, List
from numpy import random
from mesa import Agent


class Bondholder(Agent):
    """Bondholders get RLC, investment, and savings, and employment, and then decide whether to spend, save, or invest."""

    def __init__(self, model):
        # Pass the parameters to the parent class.
        super().__init__(model)
        self.USD = 10000.0  # Initial USD holdings
        self.RLC = 0.0  # Initial RLC holdings
        

    