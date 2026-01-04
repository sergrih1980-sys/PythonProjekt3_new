import pytest


@pytest.fixture
def symbol():
    return "**3456"

@pytest.fixture
def account_empty():
    return "**"
