# FILE: test_github_utils.py
import pytest
from unittest.mock import patch
from utils.github_helpers import github_user_exists

@pytest.fixture
def mock_github_user_exists():
    with patch('utils.github_helpers.github_user_exists') as mock:
        yield mock

def test_github_user_exists_true(mock_github_user_exists):
    mock_github_user_exists.return_value = True
    assert github_user_exists("existing_user") is True

def test_github_user_exists_false(mock_github_user_exists):
    mock_github_user_exists.return_value = False
    assert github_user_exists("nonexistent_user") is False