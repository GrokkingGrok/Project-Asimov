from mesa import Agent, Model
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# This line is for Agent Imports
from agents.network import BidNet, Bondholder, Daneel, Enterprise, Giskard, Isaac, RoboFund

class simulation(Model):
    def __init__(self, num_agents, seed=None):
        super().__init__(seed=seed)
        self.num_agents = num_agents