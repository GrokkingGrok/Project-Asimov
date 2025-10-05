
# Standard library imports
from typing import Optional
from mesa_frames import AgentSet
from numpy import random
from mesa import Agent
import polars as pl


class RobotSet(AgentSet):
    """Robot make Products and sell them go Bondholders."""

    def __init__(self, n: int, 
                 model, 
                 avg_value=50, 
                 avg_time=10):
        super().__init__(model)
        # Handle task_value: Default to 50 if None, then add noise
        self.avg_value = self.random.normal(avg_value, 5, n)
        self.avg_time = self.random.normal(avg_time, 2, n)
        self += pl.DataFrame(
            {
                "task_value": avg_value,
                "task_time": avg_time,
            })
        self.model.sets += self
        
    def step(self):
        """Vectorized step method for bondholder agents."""
        pass
        
        
        
        

    

    