from mesa import Agent
class Oracle(Agent):
    """
    Represents a a job being done by a robot
    """

    def __init__(self, model) -> None:  # expects mesa.Model and float amount
        # Pass the parameters to the parent class.
        super().__init__(model)
        