import pytest


@pytest.fixture
def symbol() -> str:
    return "**3456"


@pytest.fixture
def account_empty() -> str:
    return "**"

# Фикстура: базовый набор транзакций с разными валютами
@pytest.fixture
def transactions_basic():
    return [
        {
            "operationAmount": {"currency": {"code": "RUB"}},
            "description": "Покупка в магазине"
        },
        {
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод за границу"
        },
        {
            "operationAmount": {"currency": {"code": "RUB"}},
            "description": "Оплата ЖКХ"
        },
        {
            "operationAmount": {"currency": {"code": "EUR"}},
            "description": "Онлайн‑покупка"
        }
    ]
# Фикстура: одна транзакция с другой валютой
@pytest.fixture
def single_non_matching_transaction():
    return [
        {
            "operationAmount": {"currency": {"code": "USD"}},
            "id": 2
        }
    ]
# Фикстура: пустой список транзакций
@pytest.fixture
def empty_transactions():
    return []

@pytest.fixture
def transactions_with_descriptions():
    """Фикстура: транзакции со заполненным полем 'description'."""
    return [
        {"description": "Покупка продуктов"},
        {"description": "Оплата интернета"},
        {"description": "Перевод другу"}
    ]
@pytest.fixture
def empty_transactions():
    """Фикстура: пустой список транзакций."""
    return []

@pytest.fixture
def empty_range():
    """Фикстура: пустой диапазон (start > end)."""
    return 10, 5

@pytest.fixture
def large_numbers():
    """Фикстура: большие числа (близкие к 16‑значному лимиту)."""
    return 9999999999999997, 9999999999999999

@pytest.fixture
def small_range():
    """Фикстура: маленький диапазон (1–3) для базовой проверки."""
    return 1, 3
