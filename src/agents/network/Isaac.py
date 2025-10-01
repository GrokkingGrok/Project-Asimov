from mesa import Agent
from typing import Optional, List

class Isaac(Agent):
    """
    When he receives a fulfilled Oracle, Isaac mints RLC when he receives a completed 
    """

    def __init__(self, model) -> None:  # expects mesa.Model
        # Pass the parameters to the parent class.
        super().__init__(model)
        
