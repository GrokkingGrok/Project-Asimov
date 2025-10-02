import pytest
from mesa import Model, Agent
import multilevel_mesa as mlm
from asimov.agents.network.Bondholder import Bondholder

def test_bondholder_initialization() -> None:
    """Test the initialization of the Bondholder agent."""
    class TestModel(Model):
        def __init__(self):
            super().__init__()
            self.scheduler = mlm.MultiLevel_Mesa(self) # Initialize MultiLevel_Mesa scheduler for testing
            assert hasattr(self, 'scheduler')
            assert isinstance(self.scheduler, mlm.MultiLevel_Mesa)
    # Create model and add Bondholder to it.
    model = TestModel() # Instantiate the model  
    agent = Bondholder(model)  # Instantiate Bondholder agent 
    model.register_agent(agent)  # Add to scheduler to trigger unique_id assignment

    # assertions to verify correct initialization
    assert agent.unique_id is not None  # Should be auto-assigned (e.g., 1)
    assert agent.model is model # Should reference the model
    assert hasattr(agent, 'USD')  # Should have USD attribute
    assert hasattr(agent, 'RLC')  # Should have RLC attribute