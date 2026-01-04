import pytest


@pytest.fixture
def symbol() -> None:
    return "**3456"


@pytest.fixture
def account_empty() -> None:
    return "**"
