"""Tests for the Robot agent set."""
import polars as pl
import numpy as np
from unittest.mock import Mock
from mesa_frames import Model
from asimov.agents.network.robot_set import RobotSet
class ModelForTest(Model):  # Renamed to avoid pytest warning
    def __init__(self):
        super().__init__()
        assert isinstance(self, Model)
def test_robot_initialization() -> None:
    """Test RobotSet init and multi-step progress."""
    # Enhanced mock
    mock_model = Mock()
    mock_model.random = Mock()
    mock_model.random.normal = lambda mu, sigma, size, **kwargs: [mu] * size  # Fixed at mean (50 value, 10 time)
    mock_model.random.integers = lambda low, high, size, **kwargs: list(range(1, size + 1))
    
    # Init (n=2 for quick repro; times=10, so 10 steps to done)
    robots = RobotSet(n=2, model=mock_model, avg_value=50, avg_time=10)
    
    # Post-init asserts
    assert len(robots) == 2
    assert all(robots.df["task_value"] == 50.0)
    assert all(robots.df["task_time"] == 10.0)
    assert all(~robots.df["task_done"])  # All False
    assert all(robots.df["total_produced"] == 0.0)
    assert robots.df["unique_id"].to_list() == [1, 2]
    
    # Multi-step: Run 12 steps (should complete both)
    for step_num in range(12):
        robots.step()
        if step_num < 3:  # Print early for visibility
            print(f"After step {step_num + 1}:")
            print(f"  task_time: {robots.df['task_time'].to_list()}")
            print(f"  done: {robots.df['task_done'].to_list()}")
            print(f"  produced: {robots.df['total_produced'].to_list()}")
    
    # Final asserts: All done, produced 50 each
    assert all(robots.df["task_done"])
    assert all(robots.df["task_time"] <= 0)
    assert all(robots.df["total_produced"] == 50.0)
    assert len(robots) == 2  # No discards

def test_mutability():
    """Test that RobotSet is mutable and reflects changes in model.sets.do()."""
    # Minimal real model
    class TestModel(Model):
        def __init__(self):
            super().__init__()

    model = TestModel()
    mock_random = Mock()
    mock_random.normal = lambda mu, sigma, size, **kwargs: [mu] * size
    mock_random.integers = lambda low, high, size, **kwargs: np.arange(1, size + 1, dtype=np.uint64).tolist()
    model.random = mock_random

    # Init
    robots = RobotSet(n=2, model=model, avg_value=50, avg_time=10)
    robots.df = robots.df.with_columns(pl.col("unique_id").cast(pl.UInt64))
    robots._mask = pl.lit(True, dtype=pl.Boolean).repeat_by(len(robots.df))  # Post-init mask
    model.sets += robots

    print("\nInitial DF:")
    print(robots.df)

    model.sets.do("step")

    # Pre-add assert
    assert len(robots) == 2

    # Add
    new_df = pl.DataFrame({
        "task_value": [60.0],
        "task_time": [15.0],
        "task_done": [False],
    })
    if "total_produced" in robots.df.columns:
        new_df = new_df.with_columns(pl.lit(0.0).alias("total_produced"))
    robots += new_df

    # Post-add mask (crucial!)
    robots._mask = pl.lit(True, dtype=pl.Boolean).repeat_by(len(robots.df))

    # Post-add assert
    assert len(robots) == 3
    print("\nAfter add DF:")
    print(robots.df)

    robots.do("step")

    # Final assert
    print("\nFinal DF (after second step):")
    print(robots.df)
    assert len(robots) == 3
    print("Test complete: Added robot successfully; sets/step mutable.")