# Standard Library Imports
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from numpy import random
from typing import Iterator, Iterable
# Mesa Imports
from mesa import Agent, Model
from mesa.space import SingleGrid
import multilevel_mesa as mlm
# Asimov Imports
from .agents.network.Bondholder import Bondholder
from .agents.network.Enterprise import Enterprise
from .agents.network.Isaac import Isaac
from .agents.network.Robot import Robot

@staticmethod
def create_network(model) -> None:
    """Create a network of agents within the model."""
    #model.scheduler.form_group((Isaac(model), Bondholder(model)), label="NetworkAgents")

@staticmethod
def process_for_group(model: Model, items: Iterable[Agent], group_label: str) -> Iterator[tuple[str, Agent]]:
    """Yield a tuple of group_label and agent."""
    for item in items:
        yield (group_label, item)


class simulation(Model):
    def __init__(self, num_agents=10, width=25, height=25, seed=None, rng=None) -> None:
        """Initialize the simulation model with customizable agent counts and grid dimensions."""
        super().__init__(seed=seed, rng=rng)
        self.scheduler = mlm.MultiLevel_Mesa(self)
        self.num_agents = num_agents # Number of Bondholders and Robots
        self.width = width
        self.height = height
        self.seed = seed # Seed for reproducibility
        self.rng = self.random if rng is None else rng # Use provided rng or model's rng

        # Set up the grid and agents
        self.grid = SingleGrid(width, height, torus=True)  
        # self.positions = self.rng.random(size=(self.num_agents, 2)) * self.grid.width # Random positions on the grid
        # Iterable Bondholders and Enterprises
        self.bondholders = Bondholder.create_agents(self, self.num_agents)
        self.robots  = Robot.create_agents(self, self.num_agents)
        
        # Add agents to the scheduler and place them on the grid
        """for agent in self.bondholders:
            self.scheduler.add(agent)  # Add agents to the scheduler
            w = self.random.uniform(0.0, self.width)
            h = self.random.uniform(0.0, self.height)
            self.grid.place_agent(agent, [w, h])  # Place agents on the grid
            self.scheduler.shuffle_do()  # Shuffle the scheduler to randomize agent order
        for agent in self.robots:
            self.scheduler.add(agent)  # Add agents to the scheduler
            w = self.random.uniform(0.0, self.width)
            h = self.random.uniform(0.0, self.height)
            self.grid.place_agent(agent, [w, h])  # Place agents on the grid
"""


if __name__ == "__main__":
    # Main execution block
    try:
        model = RoboFund(n_projects=3, seed=42)  # Fixed seed for reproducibility
        for _ in range(5):  # Run 5 steps
            model.step()
    except Exception as e:
        print(f"Simulation failed: {e}")