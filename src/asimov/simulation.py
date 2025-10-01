# Standard Library Imports
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
# Mesa Imports
from mesa import Agent, Model
import multilevel_mesa as mlm
# Asimov Imports
from .agents.network import BidNet, Bondholder, Daneel, Enterprise, Giskard, Isaac, RoboFund

class simulation(Model):
    def __init__(self, num_agents, seed=None)  -> None:  # expects integer num_agents and float seed
        super().__init__()
        self.scheduler = mlm.MultiLevel_Mesa(self)
        self.num_agents = num_agents
        self.seed = seed