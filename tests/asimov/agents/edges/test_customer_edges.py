import numpy as np
import polars as pl

from asimov.main import Asimovian
from asimov import CustomerEdges

def test_customer_edge_set():
    """Test EdgeSet via subclass (init/add/query/schema)."""
    seed = 42
    np.random.seed(seed)
    
    model = Asimovian(num_bondholders=1, num_robots=1, num_enterprises=1, seed=seed)
    
    # Initial edges (missing sub-field—defaults added)
    initial_edges = [
        {
            "edge_type": "Customer",
            "from_type": "bondholder",
            "from_id": model.bondholders.df["unique_id"][0],
            "to_type": "enterprise",
            "to_id": model.enterprises.df["unique_id"][0],
            "created_step": 0,
            "expires_step": 0,
            "rate": 0.05,
            "step_rate_changed": 0,
            "throughput": 0.0,
            # "payment_terms" omitted—defaults to "net30"
        }
    ]
    
    # Init subclass
    edges = CustomerEdges(model, initial_edges)
    assert len(edges) == 1  # No dupe
    assert "payment_terms" in edges.df.schema  # Sub-schema extended
    assert edges.df.schema["payment_terms"] == pl.Utf8
    assert edges.df["payment_terms"][0] == "net30"  # Default added
    
    # Add edge (calls impl)
    bh_id = model.bondholders.df["unique_id"][0]
    e_id = model.enterprises.df["unique_id"][0]
    edges.add_edge("bondholder", bh_id, "enterprise", e_id, rate=0.1, payment_terms="net60")
    assert len(edges) == 2
    assert edges.df["edge_type"][1] == "Customer"
    assert edges.df["payment_terms"][1] == "net60"  # Sub-specific
    
    # Query (base method)
    bh_edges = edges.get_edges_for("bondholder", bh_id, "out")
    assert len(bh_edges) == 2  # Initial + added
    assert bh_edges["rate"][1] == 0.1  # Added rate
    assert bh_edges["payment_terms"][1] == "net60"
    
    print("SUCCESS: Subclassed EdgeSet init/add/query/schema works.")