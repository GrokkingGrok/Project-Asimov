from mesa import Model
import polars as pl
from asimov.agents.network.isaac import Isaac  # Direct import
from asimov.agents.network.bondholder_set import BondholderSet  # Direct import
from mesa.space import SingleGrid

class Simulation(Model):
    """Main simulation model that initializes Isaac, Bondholders, and the grid."""

    def __init__(self, num_bondholders=10, width=10, height=10, seed=None):
        super().__init__(seed=seed)
        self.num_bondholders = num_bondholders
        self.grid = SingleGrid(width, height, torus=True)  # Grid for spatial placement
        
        # Create Bondholders as AgentSetPolars
        positions = [(i % width, i // width) for i in range(num_bondholders)]
        self.bondholders = BondholderSet(num_bondholders, self, positions)
        #TODO create robots and add to grid
        # Create Isaac 
        self.isaac = Isaac(1, self, self.bondholders)  # Pass n_buffers=1

    def step(self):
        """Advance the simulation by one step."""
        self.bondholders.step()  # Call step on bondholders
        # Example: Isaac distributes RLC to bondholders
        if self.bondholders:
            self.bondholders.receive_rlc(10.0)  # Distribute 10 RLC to each bondholder

if __name__ == "__main__":
    from asimov.agents.network.bondholder_set import BondholderSet
    from mesa_frames import AgentSetPolars  # For model mock
    class MockModel: pass  # Dummy for init
    model = MockModel()
    bondholders = BondholderSet(3, model)  # 3 agents
    print("Before:", bondholders.agents.select(["RLC", "USD"]))
    bondholders.receive_rlc(10.0)
    print("After:", bondholders.agents.select(["RLC", "USD"]))