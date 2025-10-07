from mesa_frames import AgentSet
import polars as pl
from abc import abstractmethod

class EdgeSet(AgentSet):
    """A collection of edges between agents managed with Polars DataFrames."""
    edge_schema = {
    "edge_type": pl.Utf8,
    "from_type": pl.Utf8,
    "from_id": pl.UInt64,
    "to_type": pl.Utf8,
    "to_id": pl.UInt64,
    "created_step": pl.UInt64, 
    "expires_step": pl.UInt64,
    "rate": pl.Float64,  # Add this
    "step_rate_changed": pl.UInt64,  # Add this
    "throughput": pl.Float64,  # Add this
    "payment_terms": pl.Utf8,  # Add this

    }
    def __init__(self, model, initial_edges: list[dict] | None= None) -> None:
        """Initialize EdgeSet with optional initial edges."""
        super().__init__(model)
        df = pl.DataFrame(schema=self.edge_schema)
        if initial_edges:
            df = pl.concat([df, pl.DataFrame(initial_edges, schema=self.edge_schema)], how="vertical_relaxed")
        self += df
        print(f"Initialized EdgeSet with {len(self)} edges.")



    @abstractmethod
    def add_edge(self, from_type: str, from_id: int, to_type: str, to_id: int, **kwargs) -> None:
        """Subclass must implement type-specific add."""
        raise NotImplementedError

    def step(self) -> None:
        """Vectorized step method for edge agents."""
        pass

    def get_edges_for(self, agent_type: str, agent_id: int, direction: str = "out") -> pl.DataFrame:
        """Get outgoing/incoming edges for an agent. Arg direction defaults to 'out if empty"""
        if direction and direction == "out":
            return self.df.filter((pl.col("from_type") == agent_type) & (pl.col("from_id") == agent_id))
        else:  # "in"
            return self.df.filter((pl.col("to_type") == agent_type) & (pl.col("to_id") == agent_id))

    