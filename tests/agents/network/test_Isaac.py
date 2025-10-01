import pytest
from mesa import Model, Agent
import multilevel_mesa as mlm
from agents.network.Isaac import Isaac

def test_isaac_initialization() -> None:
    """Test the initialization of the Isaac agent."""
    class TestModel(Model):
        pass  
    # Create model and add Isaac to it.
    model = TestModel() # Instantiate the model  
    agent = Isaac(model)  # Instantiate Isaac agent 
    model.register_agent(agent)  # Add to scheduler to trigger unique_id assignment

    # assertions to verify correct initialization
    assert agent.unique_id is not None  # Should be auto-assigned (e.g., 1)
    assert agent.model is model # Should reference the model
    
