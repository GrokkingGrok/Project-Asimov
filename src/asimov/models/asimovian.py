"""
Asimov: The Robonomics Simulation Framework 0.2.0

File: ./Project-Asimov/src/asimov/models/asimovian.py
Description:
Main simulation model coordinating the RoboTorq economy as a graph, 
with Polars DF rows as nodes (bondholders, enterprises, robots) and 
edges for flows (RoboTorq distribution to Bondholders, MintRequests, etc). 
Handles steps for production, minting, growth, and data collection.

Author: Jonathan Joseph Clark @GrokkingGrok on GitHub

License: GPL-3.0
This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <https://www.gnu.org/licenses/>.

Last updated: October 10, 2025
"""
import numpy as np
import polars as pl
from mesa_frames import Model
from asimov.agents.network.bondholder_set import BondholderSet
from asimov.agents.network.enterprise_set import EnterpriseSet
from asimov.agents.network.robot_set import RobotSet
from asimov.agents.edges.customer_edges import CustomerEdges
"""
Version 0.2.0 Updates:
- ditched mesa and mesa frames, now pure polars and numpy for flexibility
- embracing networkx for graph operations
"""
class Asimovian(Model):
    """
Simulation model coordinating the RoboTorq economy.

The RoboTorq Economy thrives because:
    - Robots are bonded to Bondholders through the Bond Network.
    - Bondholders own micro-shares of every robot’s labor.
    - Enterprises procure robotic labor via the Bond Network.
    - Robots produce goods, fueling the Bond Network’s cycle.
    - Bondholders purchase robot-made products from Enterprises.
    - Isaac mints RoboTorq, scaled to robotic productivity.
    - Isaac distributes RoboTorq to Bondholders via the "disto stream."
    - Bondholders spend, save, or invest RoboTorq, perpetuating the loop.
    - See ``src/asimov/actors/`` for more info about these actors.

v0.2.0 Asmimovian Handling:
    - RoboFund, BidNet, Giskard, and Daneel are not yet implemented.
    - Isaac has bare bones functionality.
    - One enterprise, conglomoCorp, is hardcoded.
    - The Bond Network is a mock economy with
    - The first BRLA is manually created to kickstart the economy.
    - Major Step Updates only.
    - Future versions will refine updates to focus on active nodes/edges.

Here’s how the Asimovian class will eventually bring this vibrant economy to life.

asimovian.py Simulation Flow:
    - Initializes the model with parameters from ``main.py`` or ``app.py``.
    - Sets termination condition(s) for the simulation.
    - Spins up core actor nodes (RoboFund, BidNet, Daneel, Giskard, Isaac).
    - Integrates robots and bondholders from the pre-RoboTorq economy, 
    forging new edges for economic relationships.
    - Executes the initial Bonded Robot Labor Agreement (BRLA) to ignite the economy.
    - Drives major and minor updates to propagate activity through the graph.
        - Major Updates perform thorough graph updates, grafting or 
        pruning nodes as needed.
        - Minor Updates focus on active edges, inviting orphaned 
        nodes only when essential.
    - Returns results when termination conditions are met.

Eventual RoboTorq Economy AI Infrastructure/Actors:
    - RoboFund: The AI conductor of commercial investments.
        - Enterprises create Buyer or Maker Funnels tied to Projects.
        - Bondholders channel disto streams to Funnels.
        - Projects become Bids when sufficiently funded.
    - BidNet: The AI auctioneer filtering RoboFund’s offerings.
        - Evaluates Bids with Giskard and Daneel’s insights.
        - Accepts the most competitive Bids, converting them to BRLAs.
        - Sends BRLAs to Giskard for production planning.
        - See ``asimov/data/brla.py`` for details.
    - Giskard: The AI analyst averting production crises.
        - Evaluates BRLAs and creates OracleChains for the job.
        - Sends prepared BRLAs to Daneel for execution.
        - Hosts FUBAR Funnels for salvageable failing BRLAs.
    - Daneel: The AI steward of the robotic fleet.
        - Manages purchasing, deployment, repairs, and rebalancing based 
        on fleet utilization.
        - When Daneel deploys robots, it converts BRLAs to active JobSites.
        - Provides Fleet and JobSite data to other AI actors for decision-making.
    - Isaac: The AI overseer of RoboTorq’s minting and flow.
        - Processes MintRequests from Giskard via Daneel’s Oracle data.
        - Mints RoboTorq and schedules distribution through the DistoBuffer.
        - Adjusts Slow, Fast, and Warp Isaac Factors (SIF, FIF, WIF).
    - Full implementation of these actors will require a distributed cluster.
    - See ``src/asimov/ai_actors/`` for implementation details.

Asimovian Initialization:
    - Processes arguments from simulation setup to forge the Bond Network 
    within the pre-RoboTorq economy.
    - Establishes the graph structure for dynamic economic interactions.

During each Major Step Update:
    - Updates all active actors, regardless of edge connections.
    - Grafts new nodes into the network or prunes inactive ones.
    - Creates or removes edges based on node states.
    - Prepares the graph for subsequent iterations.

During each Minor Step Update (not planned in v0.2.0):
    - Propagates the cascade of activity from a Major Update.
    - Updates only nodes with connected edges.
    - Invites unconnected nodes only if required by active nodes.
    - Prunes nodes if their edges expire before the next major update.

Eventual Organic Economic Emergence:
    - The RoboTorq economy grows organically as minting scales with 
    fleet size and demand. 
    - AI actors autonomously decide to onboard robots or bondholders 
    based on growth strategies as defined in parameter files.

Looking Ahead:
    When you're comfortable with the Asimovian class, take a look
    at ``src/asimov/parameters/parquet_maker.py`` to understand how
    the initial parameter files are generated for the pre-RoboTorq economy.

    Args:
        economy_graph (nx.DiGraph): Pre-RoboTorq Economy graph. Defaults to None.
    
    Methods:
    process_parameters(): Processes and validates input parameters.
    
    
    Returns:
    
    results (pl.DataFrame): DataFrame containing collected metrics over time for analysis.

    Raises:
    FileNotFoundError: Your data file or path is malformed or missing.
    ValueError: If data files are incorrectly formatted or contain invalid data.

    Example usage:

    """
    def __init__(self, 
                 width=10,
                 height=10,
                 num_bondholders=10,
                 num_robots=1,
                 num_enterprises=1,
                 seed=None):
        super().__init__()
        # Seed RNG properly (Generator supports it)
        if seed is not None:
            self.random = np.random.default_rng(seed)  # New seeded Generator
        else:
            self.random = np.random.default_rng()  # Default unseeded
        self.width = width
        self.height = height
        # Add AgentSets to the model
        self.num_bondholders = num_bondholders
        self.bondholders = BondholderSet(num_bondholders, self)
        self.robots = RobotSet(num_robots, self)
        self.enterprises = EnterpriseSet(num_enterprises, self)
        
        self.sets += [self.bondholders, self.robots, self.enterprises]  # Register for built-in ops/tests
        self.agent_sets = [self.bondholders, self.robots, self.enterprises]  # Your manual list unchanged
        # ... (rest)
        # Example: Customer edges
        initial_customer_edges = [
        {
            "edge_type": "Customer",
            "from_type": "bondholder",
            "from_id": self.bondholders.df["unique_id"][0],  # First bondholder
            "to_type": "enterprise",
            "to_id": self.enterprises.df["unique_id"][0],
            "created_step": 0,
            "expires_step": 0,
            "rate": 0.05,
            "step_rate_changed": 0,
            "throughput": 0.0,
        }]
        self.customer_edges = CustomerEdges(self, initial_customer_edges)
        self.current_step = 0  # For timestamps
        self.sets.step()
        
    # Plan to use run_model as a loop in main, will return the DataFrame for analysis
    def run_model(self, steps) -> None:
        """Run the model for a specified number of steps."""
        for _ in range(steps):
            self.step()

    def step(self) -> None:
        self.current_step
        for agent_set in self.sets:
            self.sets.step()
            self.customer_edges.step()
        #self.enterprises.step()
        # do this for every type of agent, adding changes to self.previous_step for analysis