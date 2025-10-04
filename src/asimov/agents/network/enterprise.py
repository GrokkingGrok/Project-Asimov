import random
import polars as pl
from mesa_frames import AgentSetPolars
#from asimov.mixins.agent_helpers import generate_verts

class EnterpriseSet(AgentSetPolars):
    """An agent with fixed initial wealth."""

    def __init__(self, n: int, 
                 model, 
                 positions: list[tuple[int, int]] | None=None):
        super().__init__(model)
        #self.verts = generate_verts() TODO fix this so it will import correctly
        data = {
            "unique_id": pl.Series("unique_id", pl.arange(n, eager=True)),
            "USD": pl.Series("USD", [10000.0] * n),  
            "RLC": pl.Series("RLC", [0.0] * n),
            #"Sector": pl.Series("Sector", [random.choice(self.verts) for _ in range(n)])  
        }
        if positions and len(positions) == n:
            data["pos"] = pl.Series("pos", positions)
        else:
            data["pos"] = pl.Series("pos", [None] * n)
        self += pl.DataFrame(data)

    def step(self):
        """Vectorized step method for bondholder agents."""
        pass