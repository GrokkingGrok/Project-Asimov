from typing import Optional
from mesa_frames import AgentSet
import polars as pl

class Isaac(AgentSet):
    """An agent managing buffer items and distributing RLC to bondholders."""
    
    def __init__(self, 
                model, 
                initial_USD: float | None=None):
        super().__init__(model)
        # Initialize attributes
        initial_USD = 1000000000.0 if initial_USD is None else initial_USD
        initial_RT = 0.0
        # Create a Polars DataFrame to hold data
        self += pl.DataFrame(
            {
                "USD": initial_USD,
                "RT": initial_RT,
            })
        # Add this agent set to the model's sets
        self.model.sets += self
    def step(self):
        pass