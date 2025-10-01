from mesa import Agent
from agents.network import Bondholder, Daneel, Enterprise, Giskard, Isaac, RoboFund

class BidNet(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, model):
        # Pass the parameters to the parent class.
        super().__init__(model)