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
            })
        print(f"Initialized {n} bondholders.")
        


    def step(self) -> None:
        """Vectorized step method for bondholder agents."""
        print("Bondholders stepping...")
        self.do("work")
        pass

    def work(self) -> None:
        """Bondholders get paid for their labor."""
        print("Bondholders working...")
        self.df = self.df.with_columns(pl.col("USD") + 100)
        pass