from mesa_frames import AgentSetPolars
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
        # self.df: Accesses the underlying Polars DataFrame (standard in AgentSetPolars).
        self.agents = self.agents.with_columns([
        # pl.col("RLC") + amount: Adds amount to every row's "RLC" (broadcasts scalar).
        # .alias("RLC"): Renames back to original column.
        (pl.col("RLC") + amount).alias("RLC"),
        # Same for USD (subtract amount).
        (pl.col("USD") - amount).alias("USD")
        ])
        # Assigns to self.df: Updates the agent's data (mesa-frames tracks this).
        # Performance: Zero-copy—Polars optimizes (no data duplication, fast vectorized ops).