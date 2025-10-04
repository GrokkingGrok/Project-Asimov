"""Simulation model for the Asimov ecosystem."""
from typing import Optional

from mesa import Model
from mesa.space import SingleGrid

from asimov.agents.network.bondholder_set import BondholderSet
from asimov.agents.network.isaac import Isaac
from asimov.agents.network.robot import RobotSet


class Simulation(Model):
    """Initializes Isaac, Bondholders, and the grid."""

    def __init__(self,  
                 width=10, 
                 height=10,
                 num_bondholders=10, 
                 num_robots=1,
                 num_enterprises: Optional[int] | None=None,
                 seed: Optional[int] | None=None):
        super().__init__(seed=seed)
        self.grid = SingleGrid(width, height, torus=True)  # Grid for spatial placement
        self.num_bondholders = num_bondholders
        self.num_robots = num_robots
        
        # Create positions for each agent type
        bond_positions = [(i % width, i // width) for i in range(num_bondholders)]
        robot_positions = [(i % width, i // width) for i in range(num_bondholders)]
        # Initialize agent sets
        self.bondholders = BondholderSet(num_bondholders, self, bond_positions)
        self.robots = RobotSet(num_robots, self, robot_positions)  # Example: Same number of robots
        # Create Isaac
        self.isaac = Isaac(1, self, self.bondholders)  # Pass n_buffers=1

    def step(self):
        """Advance the simulation by one step."""
        self.bondholders.step()  # Call step on bondholders
        # Example: Isaac distributes RLC to bondholders
        if self.bondholders:
            self.bondholders.receive_rlc(10.0)  # Distribute 10 RLC to each bondholder


if __name__ == "__main__":
    class MockModel: pass  # Dummy for init
    model = MockModel()
    bondholders = BondholderSet(3, model)  # 3 agents
    print("Before:", bondholders.agents.select(["RLC", "USD"]))
    bondholders.receive_rlc(10.0)
    print("After:", bondholders.agents.select(["RLC", "USD"]))