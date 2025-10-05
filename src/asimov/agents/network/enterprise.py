import polars as pl
from mesa_frames import AgentSet

class EnterpriseSet(AgentSet):
    """An agent with fixed initial wealth."""

    def __init__(self, 
                 n: int, 
                 model):
        super().__init__(model)
        # Initialize attributes
        initial_USD = self.random.normal(50000,7000,n)
        initial_RT = 0
        # Create a Polars DataFrame to hold data
        self += pl.DataFrame(
            {
                "USD": initial_USD,
                "RT": initial_RT,
            })
        # Add this agent set to the model's sets
        self.model.sets += self
       

    def step(self):
        """Vectorized step method for bondholder agents."""
        pass