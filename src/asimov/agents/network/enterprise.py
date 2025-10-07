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
        #self.model.sets += self
       

    def step(self) -> None:
        """Vectorized step method for bondholder agents."""
        print("Enterprises stepping...")
        self.do("work")
        pass

    def work(self) -> None:
        """Enterprises get paid for their labor."""
        print("Enterprises working...")
        self.df = self.df.with_columns(pl.col("USD") + 100)
        pass