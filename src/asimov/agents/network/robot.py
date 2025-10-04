
# Standard library imports
from typing import Optional
from mesa_frames import AgentSetPolars
from numpy import random
from mesa import Agent
import polars as pl


class RobotSet(AgentSetPolars):
    """Robot make Products and sell them go Bondholders."""

    def __init__(self, n: int, 
                 model, 
                 positions: Optional[list[tuple[int, int]]] | None=None, 
                 avg_value: Optional[float]=50, 
                 avg_time: Optional[int]=10):
        super().__init__(model)
        # Handle task_value: Default to 50 if None, then add noise
        self.base_value = avg_value if avg_value is not None else 50.0
        self.base_value = random.normal(self.base_value, self.base_value / 2)  # Value of the task the robot is assigned
        self.task_time = avg_time if avg_time is not None else 10  # Time to complete the task in steps
        self.is_task_done = False # Whether the robot has completed its task always init to False
        
        # Add data to the polars
        data = {
            "unique_id": pl.Series("unique_id", pl.arange(n, eager=True)),
            "task_value": pl.Series("task_value", [self.base_value] * n),  # Evaluate to list
            "task_time": pl.Series("task_time", [self.task_time] * n),      # Evaluate to list
            "is_task_done": pl.Series("is_task_done", [False] * n),      # Evaluate to list
        }
        if positions and len(positions) == n:
            data["pos"] = pl.Series("pos", positions)
        else:
            data["pos"] = pl.Series("pos", [None] * n)
        self += pl.DataFrame(data)
        
    def step(self):
        """Vectorized step method for bondholder agents."""
        pass
        
        
        
        

    

    