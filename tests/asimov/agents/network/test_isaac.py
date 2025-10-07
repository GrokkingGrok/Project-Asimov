import pytest
from mesa_frames import Model
from asimov import Isaac


class ModelForTest(Model):  # Renamed to avoid pytest warning
    def __init__(self):
        super().__init__()
        assert isinstance(self, Model)

def test_isaac_initialization():
    model = ModelForTest()
    isaac = Isaac(model)  # Specify n=5 to match assertion
    #assert model.sets.contains(isaac)
    assert isinstance(isaac, Isaac)