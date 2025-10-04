"""Simulation model for the Asimov ecosystem."""
from typing import Optional

from mesa import Model
from mesa.space import MultiGrid


from asimov.agents.network.bondholder_set import BondholderSet
from asimov.agents.network.isaac import Isaac
from asimov.agents.network.robot import RobotSet
from asimov.agents.network.enterprise import EnterpriseSet


class Simulation(Model):
    """Initializes Isaac, Bondholders, and the grid."""

    def __init__(self,  
                 width: int=10, 
                 height: int=10,
                 num_bondholders: int=10, 
                 num_robots: int=1,
                 num_enterprises: int=2,
                 seed: Optional[int] | None=None):
        super().__init__(seed=seed)
        self.grid = MultiGrid(width, height, torus=True)  # Grid for spatial placement
        self.num_bondholders = num_bondholders
        self.num_robots = num_robots
        self.num_enterprises = num_enterprises
        
        # Create positions for each agent type
        bond_positions = [(i % width, i // width) for i in range(num_bondholders)]
        robot_positions = [(i % width, i // width) for i in range(num_robots)]
        enterprise_positions = [(i % width, i // width) for i in range(num_enterprises)]
        #TODO randomize positions? need to think about how they get on a grid.
        # Initialize agent sets, placing them on the grid.
        self.bondholders = BondholderSet(num_bondholders, self, bond_positions)
        self.robots = RobotSet(num_robots, self, robot_positions)
        self.enterprises = EnterpriseSet(num_enterprises, self, enterprise_positions)
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