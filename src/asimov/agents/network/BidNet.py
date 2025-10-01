from mesa import Agent

class BidNet(Agent):
    """BidNet is the networks arbiter in the bidding process."""

    def __init__(self, model):
        # Pass the parameters to the parent class.
        super().__init__(model)