from unittest.mock import Mock
from mesa_frames import Model
from asimov.agents.network.bondholder_set import BondholderSet

class ModelForTest(Model):  # Renamed to avoid pytest warning
    def __init__(self):
        super().__init__()
        assert isinstance(self, Model)

def test_bondholder_initialization():
    # Enhanced mock (same as debug)
    mock_model = Mock()
    mock_model.random = Mock()
    mock_model.random.uniform = lambda low, high, size, **kwargs: [5000.0] * size
    mock_model.random.integers = lambda low, high, size, **kwargs: list(range(1, size + 1))
    
    # Init
    bondholders = BondholderSet(n=3, model=mock_model)
    
    # Asserts: Post-init state
    assert len(bondholders) == 3
    assert "USD" in bondholders.df.columns
    assert "unique_id" in bondholders.df.columns
    assert all(bondholders.df["USD"] == 5000.0)  # From mock
    assert bondholders.df["unique_id"].to_list() == [1, 2, 3]
    
    # Step (prints should show with -s)
    bondholders.step()
    
    # Post-step assert (add real logic to work() for more)
    assert len(bondholders) == 3  # No discards yet

    # In test_bondholder_initialization_and_step(), after bondholders.step()
    assert all(bondholders.df["USD"] == 5100.0)  # 5000 + 100   

