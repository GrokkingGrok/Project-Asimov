from mesa import Agent
from typing import Optional, List

class Isaac(Agent):
    """
    Fulfilled Oracles send MintRequests to Isaac, who mints RLC and adds it to his distoBuffer.
    """

    def __init__(self, model) -> None:  # expects mesa.Model
        # Pass the parameters to the parent class.
        super().__init__(model)
        

