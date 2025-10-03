
# Standard library imports
from typing import Optional, List
from numpy import random
from mesa import Agent


class Robot(Agent):
    """Robot make Products and sell them go Bondholders."""

    def __init__(self, model):
        # Pass the parameters to the parent class.
        super().__init__(model)
        self.taskValue = random.normal(25.0, 5.0)  # Value of the task the robot is assigned
        self.taskDone = False

    

    