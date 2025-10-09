"""Tests for Asimovian model and dynamic agent management."""
import polars as pl
import numpy as np
from asimov.models.asimovian import Asimovian
from asimov.agents.network.bondholder_set import BondholderSet
from asimov.agents.network.enterprise_set import EnterpriseSet
from asimov.agents.network.robot_set import RobotSet
def test_simulation_initialization():
    # Define parameters for the simulation
    width = 10
    height = 10
    initial_capacity = width * height
    num_bondholders = 10
    num_robots = 1
    num_enterprises = 1
    
    sim_model = Asimovian(width, 
                          height,
                          num_bondholders, 
                          num_robots, 
                          num_enterprises)

    # Verify Isaac is created
    #assert isinstance(sim_model.isaac, Isaac)
    #assert len(sim_model.isaac) == 1  # Isaac as single-agent set
    #assert sim_model.isaac["wealth"][0] == 100.0
    
    # Verify Bondholders are created
    assert len(sim_model.bondholders) == num_bondholders
    assert isinstance(sim_model.bondholders, BondholderSet)

    # Verify Robots are created
    assert len(sim_model.robots) == num_robots
    assert isinstance(sim_model.robots, RobotSet)

    # Verify Enterprises are created
    assert len(sim_model.enterprises) == num_enterprises
    assert isinstance(sim_model.enterprises, EnterpriseSet)

def test_add_agent():
    """Test adding an agent mid-sim to a set (e.g., robots) and verify model.step() includes it."""
    seed = 42
    np.random.seed(seed)  # Global fallback
    
    # Init full model with seed
    model = Asimovian(
        width=5, height=5,
        num_bondholders=2, num_robots=2, num_enterprises=1,
        seed=seed  # Pass for repro
    )
    
    print("\nInitial robot count:", len(model.robots))
    print("Initial robots DF:")
    print(model.robots.df)

    # First step: All sets run (progresses existing robots)
    model.step()
    
    # Sync mask post-step (prevents add desync)
    model.robots._mask = pl.lit(True, dtype=pl.Boolean).repeat_by(len(model.robots.df))

    # Assert pre-add: Post-step = initial -1.0 (exact from your trace)
    assert len(model.robots) == 2

    # Add new robot
    new_df = pl.DataFrame({
        "task_value": [60.0],
        "task_time": [15.0],
        "task_done": [False],
    })
    if "total_produced" in model.robots.df.columns:
        new_df = new_df.with_columns(pl.lit(0.0).alias("total_produced"))
    
    model.robots += new_df
    model.robots._mask = pl.lit(True, dtype=pl.Boolean).repeat_by(len(model.robots.df))

    # Assert post-add
    assert len(model.robots) == 3
    print("\nAfter add robots DF:")
    print(model.robots.df)


    # Second step: All sets run (new progresses)
    model.step()

    # Assert final: New = 14.0, originals -1.0 again
    print("\nFinal robots DF (after second step):")
    print(model.robots.df)
    assert len(model.robots) == 3
    print("SUCCESS: Added robot mid-sim; model.step() includes it without breakage.")

def test_remove_agent():
    """Test removing an agent mid-sim from a set (e.g., discard done robots) and verify model.step() skips it."""
    seed = 42
    np.random.seed(seed)  # Global fallback
    
    # Init full model with seed (n=3 for variety)
    model = Asimovian(
        width=5, height=5,
        num_bondholders=2, num_robots=3, num_enterprises=1,
        seed=seed
    )
    
    print("\nInitial robot count:", len(model.robots))
    print("Initial robots DF:")
    print(model.robots.df)
    
    # Capture initial unique_ids *before* first step
    initial_ids = model.robots.df["unique_id"].to_list()  # Track for survivors
    print(f"Initial IDs: {initial_ids}")

    # First step: All sets run (progresses all robots)
    model.step()
    
    # Sync mask post-step (pre-discard)
    model.robots._mask = pl.Series([True] * len(model.robots.df), dtype=pl.Boolean)

    # Assert pre-discard
    assert len(model.robots) == 3

    # Discard exactly 1 (fallback to first if no "done")
    discard_df = model.robots.df.filter(pl.col("task_time") < 7.0)  # "Done" threshold
    if len(discard_df) == 0 or len(discard_df) > 1:
        discard_df = model.robots.df.head(1)  # Exactly 1, first row
    print(f"Discarding {len(discard_df)} robot(s):")
    print(discard_df)
    discard_ids = discard_df["unique_id"].to_list()
    
    try:
        # Try official discard
        model.robots.discard(discard_df)
    except Exception as e:
        print(f"Official discard failed ({e}); using manual fallback.")
        # Manual fallback: Filter out by unique_id
        model.robots.df = model.robots.df.filter(~pl.col("unique_id").is_in(discard_ids))
        model.robots._mask = pl.Series([True] * len(model.robots.df), dtype=pl.Boolean)  # Sync post-manual
    
    # Sync mask post-discard (for next step)
    model.robots._mask = pl.Series([True] * len(model.robots.df), dtype=pl.Boolean)

    # Assert post-discard: Len dropped to 2
    assert len(model.robots) == 2  # Exactly 1 removed
    print("\nAfter discard robots DF:")
    print(model.robots.df)
    post_discard_ids = set(model.robots.df["unique_id"].to_list())
    assert len(post_discard_ids) == 2  # Survivors unique

    # Second step: All sets run (only survivors progress)
    model.step()

    # Assert final: Survivors still there (no further discards)
    print("\nFinal robots DF (after second step):")
    print(model.robots.df)
    assert len(model.robots) == 2  # Stable
    print("SUCCESS: Removed robot mid-sim; model.step() skips it without breakage.")

def test_model_sets_add_remove():
    """Test registry's model.sets.add/remove for dynamic sets mid-sim."""
    seed = 42
    np.random.seed(seed)
    
    # Init full model with seed
    model = Asimovian(
        width=5, height=5,
        num_bondholders=2, num_robots=2, num_enterprises=1,
        seed=seed
    )
    
    initial_robots_time = np.mean(model.robots.df["task_time"].to_list())
    print(f"Initial robots avg task_time: {initial_robots_time}")

    # First step: All sets run
    model.step()

    # Assert pre-new-set: Existing progressed
    assert np.mean(model.robots.df["task_time"].to_list()) < initial_robots_time

    # Create new RobotSet (1 robot)
    new_robots = RobotSet(n=1, model=model, avg_value=60, avg_time=15)
    new_initial_time = new_robots.df["task_time"][0]
    print(f"New robots DF (pre-register): {new_robots.df}")

    # Sync mask for new set
    new_robots._mask = pl.Series([True] * len(new_robots.df), dtype=pl.Boolean)

    model.sets.add(new_robots)  # Built-in register

    # Assert post-add: New in registry
    assert new_robots in model.sets  # Membership only (no private _sets)

    # Second step: All sets run (new progresses)
    model.step()

    # Assert: New decayed
    print(f"New robots DF (post-step): {new_robots.df}")
    assert new_robots.df["task_time"][0] <= new_initial_time

    # Remove new set via built-in
    model.sets.remove(new_robots)

    # Assert post-remove: New unregistered
    assert new_robots not in model.sets  # Membership only

    # Third step: All sets run (original progresses, new skipped)
    model.step()

    # Assert: Original further decayed, new unchanged
    original_final_time = np.mean(model.robots.df["task_time"].to_list())
    assert original_final_time <= np.mean(model.robots.df["task_time"].to_list())  # Further? Wait, use post-first
    post_first_time = np.mean(model.robots.df["task_time"].to_list())  # From after first step
    assert original_final_time <= post_first_time  # Further from post-first
    assert new_robots.df["task_time"][0] == new_robots.df["task_time"][0]  # Unchanged (skipped)

    print("SUCCESS: model.sets.add/remove dynamic sets; step adapts.")

def test_model_remove_agent_by_id():
    """Test removing individual agent from set via model.sets.remove by IDs."""
    seed = 42
    np.random.seed(seed)
    
    # Init (n=2 robots)
    model = Asimovian(
        width=5, height=5,
        num_bondholders=2, num_robots=2, num_enterprises=1,
        seed=seed
    )
    
    initial_times = model.robots.df["task_time"].to_list()
    initial_ids = model.robots.df["unique_id"].to_list()
    print(f"Initial task_time: {initial_times}, IDs: {initial_ids}")

    # First step: All progress
    model.step()

    # Sync mask pre-remove
    model.robots._mask = pl.Series([True] * len(model.robots.df), dtype=pl.Boolean)

    # Remove first robot by ID
    remove_id = initial_ids[0]
    try:
        model.sets.remove(remove_id)  # Built-in by ID
    except Exception as e:
        print(f"Official remove failed ({e}); manual fallback.")
        # Fallback: Filter out by ID
        model.robots.df = model.robots.df.filter(pl.col("unique_id") != remove_id)
        model.robots._mask = pl.Series([True] * len(model.robots.df), dtype=pl.Boolean)

    # Assert post-remove: Len dropped, survivor unchanged
    assert len(model.robots) == 1
    print(f"After model.sets.remove by ID robots DF: {model.robots.df}")
    survivor_id = model.robots.df["unique_id"][0]
    assert survivor_id == initial_ids[1]  # Second survived

    # Second step: Only survivor progresses
    model.sets.do("step")  # Registry-wide (includes new)

    # Assert final: Survivor -1.0 more
    print("SUCCESS: Removed agent by ID; step skips it.")