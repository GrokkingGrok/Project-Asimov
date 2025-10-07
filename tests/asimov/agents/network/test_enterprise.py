import pytest
import polars as pl
from unittest.mock import Mock
from asimov import EnterpriseSet  # Adjust path as needed

def test_enterprise_initialization():
    """Test EnterpriseSet init and step with prints visible."""
    # Enhanced mock (stubs for normal, integers; uniform if used later)
    mock_model = Mock()
    mock_model.random = Mock()
    mock_model.random.normal = lambda mu, sigma, size, **kwargs: [mu] * size  # Fixed at mean (50000.0) for repro
    mock_model.random.integers = lambda low, high, size, **kwargs: list(range(1, size + 1))  # 1,2,3... for IDs
    mock_model.random.uniform = lambda low, high, size, **kwargs: [5000.0] * size  # Fallback if needed
    
    # Init
    enterprises = EnterpriseSet(n=5, model=mock_model)
    
    # Asserts: Post-init state
    assert len(enterprises) == 5
    assert "USD" in enterprises.df.columns
    assert "RT" in enterprises.df.columns  # From your init
    assert "unique_id" in enterprises.df.columns
    assert all(enterprises.df["USD"] == 50000.0)  # From mock (mean)
    assert all(enterprises.df["RT"] == 0.0)  # Initial zeros
    assert enterprises.df["unique_id"].to_list() == [1, 2, 3, 4, 5]
    
    # Step (prints should show with -s; assumes step/do/work exist like bondholder)
    enterprises.step()
    
    # Post-step assert (add real logic to work() for more, e.g., USD += rev)
    assert len(enterprises) == 5  # No discards yet