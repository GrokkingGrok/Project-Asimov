"""Bondholder agent set using Polars DataFrames for efficient management."""
from mesa_frames import AgentSet

import polars as pl


class BondholderSet(AgentSet):
    """A collection of bondholder agents managed with Polars DataFrames.
        
        
    """
    def __init__(self, 
                 n: int, 
                 model,
                 ):
        super().__init__(model)
        # Initialize attributes
        initial_USD = self.random.uniform(2000.0,10000.0,n)
        initial_RT = 0.0
        # Create a Polars DataFrame to hold data
        self += pl.DataFrame(
            {
                "USD": initial_USD,
                "RT": initial_RT,
            })
        # Add this agent set to the model's sets
        self.model.sets += self
        
        

    def step(self) -> None:
        """Vectorized step method for bondholder agents."""
        pass
