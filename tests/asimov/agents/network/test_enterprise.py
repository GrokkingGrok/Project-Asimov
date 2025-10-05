import pytest
from mesa_frames import Model
from asimov import EnterpriseSet

class ModelForTest(Model):  # Renamed to avoid pytest warning
    def __init__(self):
        super().__init__()
        #assert isinstance(self, Model)

def test_enterprise_initialization() -> None:
    """Test the initialization of the Enterprise agent."""
    model = ModelForTest()
    enterprises = EnterpriseSet(5, model)  # Specify n=5 to match assertion
    assert model.sets.contains(enterprises)
    assert isinstance(enterprises, EnterpriseSet)