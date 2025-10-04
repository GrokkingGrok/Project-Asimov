import pytest
from mesa import Model
from asimov import BondholderSet

class ModelForTest(Model):  # Renamed to avoid pytest warning
    def __init__(self):
        super().__init__()
        assert isinstance(self, Model)

def test_bondholder_initialization():
    model = ModelForTest()
    bondholders = BondholderSet(5, model)  # Specify n=5 to match assertion
    assert len(bondholders) == 5
    assert isinstance(bondholders, BondholderSet)

