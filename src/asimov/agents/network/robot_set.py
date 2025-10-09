
# Standard library imports
from typing import Optional
from mesa_frames import AgentSet
from numpy import random
from mesa import Agent
import polars as pl


class RobotSet(AgentSet):
    """Robots make Products and sell them to Bondholders."""

    def __init__(self, n: int, 
                 model, 
                 avg_value=50, 
                 avg_time=10):
        super().__init__(model)
        # Generate attributes with noise
        task_value = self.random.normal(avg_value, 5.0, n)
        task_time = self.random.normal(avg_time, 2.0, n)
        task_done = [False] * n  # Initial state as list (Polars will infer bool)
        total_produced = [0.0] * n  # Track cumulative output
        
        self += pl.DataFrame(
            {
                "task_value": task_value,
                "task_time": task_time,
                "task_done": task_done,
                "total_produced": total_produced,
            }
        )
        print(f"Initialized {n} robots.")

    def step(self) -> None:
        """Vectorized step method for robot agents."""
        print("Robots stepping...")
        self.do("work")

    def work(self) -> None:
        """Robots make progress on tasks: decrement time until done, then produce value."""
        print("Robots working...")
        # Vectorized: Progress only if not done
        progress_mask = ~pl.col("task_done") & (pl.col("task_time") > 0)
        
        self.df = self.df.with_columns([
            # Decrement task_time by 1.0 if working (linear progress; or *0.9 for decay)
            pl.when(progress_mask)
              .then(pl.col("task_time") - 5.0)
              .otherwise(pl.col("task_time"))
              .alias("task_time"),
            
            # Set done when time <=0
            pl.when((~pl.col("task_done")) & (pl.col("task_time") <= 0))
              .then(True)
              .otherwise(pl.col("task_done"))
              .alias("task_done"),
            
            # Add task_value to total_produced when newly done
            pl.when((~pl.col("task_done")) & (pl.col("task_time") <= 0))  # Newly completing
              .then(pl.col("total_produced") + pl.col("task_value"))
              .otherwise(pl.col("total_produced"))
              .alias("total_produced"),
        ])
        
        # Optional: Print summary (e.g., % done)
        done_count = self.df["task_done"].sum()
        print(f"  - {done_count}/{len(self)} robots done this step.")
        # Self-heal mask after mutation (prevents desync for adds/discards)
        self._mask = pl.lit(True, dtype=pl.Boolean).repeat_by(len(self.df))