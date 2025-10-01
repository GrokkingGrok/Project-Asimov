from mesa import Model, Agent

class Isaac(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, model):
        # Pass the parameters to the parent class.
        super().__init__(model)
        self.model: Model = model
        self.unique_id: int = next(self._ids[model])
        self.model.register_agent(self)