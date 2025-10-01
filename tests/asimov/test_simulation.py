import asimov

from asimov.simulation import simulation

def test_version() -> None: # Check that the version is correct
    assert asimov.__version__ == "0.1.0"

def test_simulation_initialization() -> None:
    """Test the initialization of the simulation model."""
    num_agents = 10
    seed = 42.0
    sim_model = simulation(num_agents, seed)
    
    # assertions to verify correct initialization
    assert sim_model.num_agents == num_agents
    assert sim_model.seed == seed
    assert hasattr(sim_model, 'scheduler')
    assert isinstance(sim_model.scheduler, asimov.simulation.mlm.MultiLevel_Mesa)