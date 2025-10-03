from mesa import Agent
class MintRequest(Agent):
    """
    Represents a request to mint RLC tokens.
    """

    def __init__(self, model) -> None:  # expects mesa.Model and float amount
        # Pass the parameters to the parent class.
        super().__init__(model)
        