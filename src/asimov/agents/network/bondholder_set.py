from mesa_frames import AgentSetPolars, AgentsDF
import polars as pl

class BondholderSet(AgentSetPolars):
    """A collection of bondholder agents managed with Polars DataFrames."""
    
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

    def receive_rlc(self, amount: float):
        """Vectorized method to receive RLC from Isaac."""
        self.update({"RLC": self["RLC"] + amount, "USD": self["USD"] - amount})