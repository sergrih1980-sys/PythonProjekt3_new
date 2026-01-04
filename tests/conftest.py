import pytest


@pytest.fixture
def symbol() -> str:
    return "**3456"


@pytest.fixture
def account_empty() -> str:
    return "**"
