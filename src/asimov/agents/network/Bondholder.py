from mesa import Agent
from typing import Optional, List

class Bondholder(Agent):
    """Bondholders get RLC, investment, and savings, and employment, and then decide whether to spend, save, or invest."""

    def __init__(self, model):
        # Pass the parameters to the parent class.
        super().__init__(model)