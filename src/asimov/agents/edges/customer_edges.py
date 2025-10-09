
from asimov.agents.edges.edge_set import EdgeSet
import polars as pl
import numpy as np
class CustomerEdges(EdgeSet):
    """Edges for customer relationships (e.g., bondholder-enterprise)."""
    def __init__(self, model, initial_edges: list[dict] | None=None) -> None:
        super().__init__(model, initial_edges)  # Base adds initial + unique_id
    
        # Extend base schema before super (so super uses it)
        schema = EdgeSet.edge_schema.copy()  # Class attr copy
        schema["payment_terms"] = pl.Utf8  # Add sub-specific
        self.edge_schema = schema  # Set instance
    
        # Add sub-field in-place to existing df (keeps unique_id)
        self.df = self.df.with_columns(pl.lit("net30").alias("payment_terms").cast(pl.Utf8))  # Default for all rows
        # Sync mask post-update (safety)
        self._mask = pl.Series([True] * len(self.df), dtype=pl.Boolean)
    
        print(f"Initialized CustomerEdges with {len(self)} edges.")

    def add_edge(self, from_type: str, from_id: int, to_type: str, to_id: int,
                 rate: float = 0.0, expires_step: int = 0, throughput: float = 0.0,
                 payment_terms: str = "net30") -> None:
        """Add customer edge with sub-specific param."""
        row = pl.DataFrame({
            "edge_type": ["Customer"],
            "from_type": [from_type],
            "from_id": [from_id],
            "to_type": [to_type],
            "to_id": [to_id],
            "created_step": [self.model.current_step],
            "expires_step": [expires_step],
            "rate": [rate],
            "step_rate_changed": [self.model.current_step],
            "throughput": [throughput],
            "payment_terms": [payment_terms],  # Sub-specific
        }, schema=self.edge_schema)
        self += row  # Triggers unique_id add
        print(f"Added customer edge {from_type}:{from_id} → {to_type}:{to_id} (rate={rate}, terms={payment_terms})")

    def step(self) -> None:
        """Vectorized step method for edge agents."""
        pass