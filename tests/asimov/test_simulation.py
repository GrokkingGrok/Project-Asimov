import pytest
from mesa.space import SingleGrid
from asimov.agents.network.bondholder_set import BondholderSet
from asimov.agents.network.isaac import Isaac
from asimov.simulation import Simulation
def test_simulation_initialization():
    num_bondholders = 10
    width = 10
    height = 10
    sim_model = Simulation(num_bondholders=num_bondholders, width=width, height=height)
    
    # Verify Isaac is created
    assert isinstance(sim_model.isaac, Isaac)
    assert len(sim_model.isaac) == 1  # Isaac as single-agent set
    assert sim_model.isaac["wealth"][0] == 100.0
    
    # Verify Bondholders are created and placed
    assert len(sim_model.bondholders) == num_bondholders
    assert isinstance(sim_model.bondholders, BondholderSet)  # Check that bondholders is a BondholderSet instance

    # Verify grid setup
    assert isinstance(sim_model.grid, SingleGrid)
    assert sim_model.grid.width == width
    assert sim_model.grid.height == height
    assert sim_model.grid.torus is True