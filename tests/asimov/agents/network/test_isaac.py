import pytest
from mesa import Model
from asimov.agents.network.isaac import Isaac


class ModelForTest(Model):  # Renamed to avoid pytest warning
    def __init__(self):
        super().__init__()
        assert isinstance(self, Model)

def test_isaac_initialization():
    model = ModelForTest()
    isaac = Isaac(1, model)  # Provide n_buffers=1
    assert isinstance(isaac, Isaac)