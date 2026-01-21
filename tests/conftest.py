from typing import Any, Dict, List, Tuple

import pytest


@pytest.fixture
def symbol() -> str:
    """Фикстура: строка с маской номера счёта."""
    return "**3456"


@pytest.fixture
def account_empty() -> str:
    """Фикстура: пустая маска счёта."""
    return "**"


@pytest.fixture
def transactions_basic() -> List[Dict[str, Any]]:
    """
    Фикстура: базовый набор транзакций с разными валютами.
    Содержит транзакции в RUB, USD, EUR.
    """

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


@pytest.fixture
def single_non_matching_transaction() -> List[Dict[str, Any]]:
    """
    Фикстура: одна транзакция с валютой, не совпадающей с целевой.
    Используется для проверки фильтрации.
    """

    return [
        {
            "operationAmount": {"currency": {"code": "USD"}},
            "id": 2
        }
    ]


@pytest.fixture
def transactions_with_descriptions() -> List[Dict[str, Any]]:
    """Фикстура: транзакции со заполненным полем 'description'."""
    return [
        {"description": "Покупка продуктов"},
        {"description": "Оплата интернета"},
        {"description": "Перевод другу"}
    ]


@pytest.fixture
def transactions_without_descriptions() -> List[Dict[str, Any]]:
    """Фикстура: транзакции без поля 'description'."""
    return [{}, {"amount": 1000}, {"id": 123, "date": "2023-01-01"}]


@pytest.fixture
def mixed_transactions() -> List[Dict[str, Any]]:
    """Фикстура: смешанный набор транзакций (с описанием и без)."""
    return [
        {"description": "Зарплата"},
        {},
        {"description": "Кафе"},
        {"category": "Развлечения"},
        {"description": ""}
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура: пустой список транзакций."""
    return []


@pytest.fixture
def single_transaction_with_description() -> List[Dict[str, Any]]:
    """Фикстура: одна транзакция с описанием."""
    return [{"description": "Единственный платёж"}]


@pytest.fixture
def single_transaction_without_description() -> List[Dict[str, Any]]:
    """Фикстура: одна транзакция без описания."""
    return [{}]


@pytest.fixture
def range_single() -> Tuple[int, int]:
    """Фикстура: диапазон из одного числа (граничный случай)."""
    return 42, 42


@pytest.fixture
def edge_cases() -> List[Tuple[int, int]]:
    """Фикстура: набор граничных случаев для параметризации."""
    return [
        (1, 1),
        (0, 0),
        (9999999999999999, 9999999999999999),
        (10000000000000000, 10000000000000000)
    ]


@pytest.fixture
def empty_range() -> Tuple[int, int]:
    """Фикстура: пустой диапазон (например, 10, 9)."""
    return 10, 9  # start > end → пустой диапазон


@pytest.fixture
def small_range() -> Tuple[int, int]:
    """Фикстура: небольшой диапазон (например, 1, 3)."""
    return 1, 3
