import pytest
from mesa import Model, Agent
from agents.network.Isaac import Isaac

def test_isaac_initialization():
    # Create a minimal model for testing (Mesa requires this)
    class TestModel(Model):
        pass
    
    model = TestModel()
    
    # Instantiate Isaac agent (unique_id is auto-assigned by Mesa)
    agent = Isaac(model)
    model.register_agent(agent)  # Add to scheduler to trigger unique_id assignment
    assert agent.unique_id is not None  # Should be auto-assigned (e.g., 1)
    assert agent.model is model