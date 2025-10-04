from mesa.space import MultiGrid
from asimov.simulation import Simulation
from asimov import Isaac, BondholderSet, EnterpriseSet, RobotSet
def test_simulation_initialization():
    
    width = 10
    height = 10
    num_bondholders = 10
    num_robots = 1
    num_enterprises = 1
    
    sim_model = Simulation(width, height, num_bondholders, num_robots, num_enterprises)
    
    # Verify grid setup
    assert isinstance(sim_model.grid, MultiGrid)
    assert sim_model.grid.width == width
    assert sim_model.grid.height == height
    assert sim_model.grid.torus is True

    # Verify Isaac is created
    assert isinstance(sim_model.isaac, Isaac)
    assert len(sim_model.isaac) == 1  # Isaac as single-agent set
    assert sim_model.isaac["wealth"][0] == 100.0
    
    # Verify Bondholders are created
    assert len(sim_model.bondholders) == num_bondholders
    assert isinstance(sim_model.bondholders, BondholderSet)

    # Verify Robots are created
    assert len(sim_model.robots) == num_robots
    assert isinstance(sim_model.robots, RobotSet)

    # Verify Enterprises are created
    #assert len(sim_model.enterprises) == num_enterprises
    #assert isinstance(sim_model.enterprises, EnterpriseSet)

    