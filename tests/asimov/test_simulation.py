from asimov.simulation import simulation
from asimov.agents.network.Isaac import Isaac
from asimov.agents.network.Bondholder import Bondholder
from asimov.agents.network.Enterprise import Enterprise
from asimov.agents.network.Robot import Robot

import asimov
# Mesa Imports
from mesa.space import SingleGrid
import multilevel_mesa as mlm

def test_version() -> None: # Check that the version is correct
    assert asimov.__version__ == "0.1.0"

def test_simulation_initialization() -> None:
    """Test the initialization of the simulation model."""
    num_agents = 10
    seed = 42.0
    x = 25
    y = 25
    sim_model = simulation(num_agents, x, y, seed)
    
    # assertions to verify correct basic initialization
    assert sim_model.num_agents == num_agents
    assert sim_model.seed == seed
    assert hasattr(sim_model, 'scheduler')
    assert isinstance(sim_model.scheduler, mlm.MultiLevel_Mesa)

    # assertions to verify bondholder and robot agents
    # Verify agent lists are intact
    assert len(sim_model.bondholders) == num_agents
    assert len(sim_model.robots) == num_agents
    assert all(isinstance(agent, Bondholder) for agent in sim_model.bondholders)
    assert all(isinstance(agent, Robot) for agent in sim_model.robots)

    # Verify grid setup
    assert isinstance(sim_model.grid, SingleGrid)
    assert sim_model.grid.width == x
    assert sim_model.grid.height == y
    assert sim_model.grid.torus is True