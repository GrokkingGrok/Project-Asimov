
import numpy as np
import polars as pl
from mesa_frames import Model
from asimov.agents.network.bondholder_set import BondholderSet
from asimov.agents.network.enterprise_set import EnterpriseSet
from asimov.agents.network.robot_set import RobotSet
from asimov.agents.edges.customer_edges import CustomerEdges


class Asimovian(Model):
    """Main model class for the Asimov simulation."""
    def __init__(self, 
                 width=10,
                 height=10,
                 num_bondholders=10,
                 num_robots=1,
                 num_enterprises=1,
                 seed=None):
        super().__init__()
        # Seed RNG properly (Generator supports it)
        if seed is not None:
            self.random = np.random.default_rng(seed)  # New seeded Generator
        else:
            self.random = np.random.default_rng()  # Default unseeded
        self.width = width
        self.height = height
        # Add AgentSets to the model
        self.num_bondholders = num_bondholders
        self.bondholders = BondholderSet(num_bondholders, self)
        self.robots = RobotSet(num_robots, self)
        self.enterprises = EnterpriseSet(num_enterprises, self)
        
        self.sets += [self.bondholders, self.robots, self.enterprises]  # Register for built-in ops/tests
        self.agent_sets = [self.bondholders, self.robots, self.enterprises]  # Your manual list unchanged
        # ... (rest)
        # Example: Customer edges
        initial_customer_edges = [
        {
            "edge_type": "Customer",
            "from_type": "bondholder",
            "from_id": self.bondholders.df["unique_id"][0],  # First bondholder
            "to_type": "enterprise",
            "to_id": self.enterprises.df["unique_id"][0],
            "created_step": 0,
            "expires_step": 0,
            "rate": 0.05,
            "step_rate_changed": 0,
            "throughput": 0.0,
        }]
        self.customer_edges = CustomerEdges(self, initial_customer_edges)
        self.current_step = 0  # For timestamps
        self.sets.step()
        
    # Plan to use run_model as a loop in main, will return the DataFrame for analysis
    def run_model(self, steps) -> None:
        """Run the model for a specified number of steps."""
        for _ in range(steps):
            self.step()

    def step(self) -> None:
        self.current_step += 1
        for agent_set in self.sets:
            agent_set.step()
            self.customer_edges.step()
        #self.enterprises.step()
        # do this for every type of agent, adding changes to self.previous_step for analysis