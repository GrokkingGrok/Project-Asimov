import polars as pl
from mesa_frames import AgentSetPolars

class EnterpriseSet(AgentSetPolars):
    """An agent with fixed initial wealth."""

    def __init__(self, n: int, model, positions: list[tuple[int, int]] | None = None):
        super().__init__(model)
        data = {
            "unique_id": pl.Series("unique_id", pl.arange(n, eager=True)),
            "USD": pl.Series("USD", [10000.0] * n),  # Evaluate to list
            "RLC": pl.Series("RLC", [0.0] * n),      # Evaluate to list
        }
        if positions and len(positions) == n:
            data["pos"] = pl.Series("pos", positions)
        else:
            data["pos"] = pl.Series("pos", [None] * n)
        self += pl.DataFrame(data)

    def step(self):
        """Vectorized step method for bondholder agents."""
        pass