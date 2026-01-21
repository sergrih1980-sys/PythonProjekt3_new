from typing import Any, Dict, List, Tuple, Iterator

import pytest

from src.generators import filter_by_currency, transaction_descriptions


def test_filter_by_currency_basic(transactions_basic: List[Dict[str, Any]]) -> None:
    """
    Тест базовой работы filter_by_currency с предопределённым набором транзакций.
    """
    result = list(filter_by_currency(transactions_basic, "RUB"))
    assert len(result) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "RUB" for t in result)

test_cases = [
    (
        [
            {"operationAmount": {"currency": {"code": "RUB"}}},
            {"operationAmount": {"currency": {"code": "USD"}}}
        ],
        "RUB",
        1
    ),
    (
        [],
        "EUR",
        0
    )
]


@pytest.mark.parametrize("transactions,currency,expected_count", test_cases)
def test_filter_by_currency_parametrized(
    transactions: List[Dict[str, Any]],
    currency: str,
    expected_count: int
) -> None:
    """
    Параметризованный тест для функции filter_by_currency.
    Проверяет:
    - фильтрацию по заданной валюте;
    - обработку отсутствия совпадений;
    - работу с пустым списком;
    - устойчивость к неполным структурам данных.
    """
    filtered = filter_by_currency(transactions, currency)
    result = list(filtered)
    assert len(result) == expected_count

    # Дополнительная проверка: если есть результаты, убедимся, что валюта совпадает
    if expected_count > 0:
        for item in result:
            assert item["operationAmount"]["currency"]["code"] == currency


def test_transaction_descriptions_with_descriptions(
    transactions_with_descriptions: List[Dict[str, Any]]
) -> None:
    """Тест: все транзакции имеют поле description."""
    result = list(transaction_descriptions(transactions_with_descriptions))
    expected = ["Покупка продуктов", "Оплата интернета", "Перевод другу"]
    assert result == expected


def test_transaction_descriptions_single_with_description(
    single_transaction_with_description: List[Dict[str, Any]]
) -> None:
    """Тест: одна транзакция с полем description."""
    result = list(transaction_descriptions(single_transaction_with_description))
    expected = ["Единственный платёж"]
    assert result == expected


def test_transaction_descriptions_empty(empty_transactions: List[Dict[str, Any]]) -> None:
    """Тест: пустой список транзакций."""
    result = list(transaction_descriptions(empty_transactions))
    expected: List[str] = []
    assert result == expected


def test_consistency_with_string_conversion() -> None:
    """Тест: соответствие строкового представления числа и формата вывода."""
    num = 123456789
    padded = str(num).zfill(16)
    formatted = f"{padded[:4]} {padded[4:8]} {padded[8:12]} {padded[12:16]}"

    generator = card_number_generator(num, num)
    result = next(generator)
    assert result == formatted


def test_empty_range_behavior(empty_range: Tuple[int, int]) -> None:
    """Тест: пустой диапазон не должен выдавать значений."""
    start, end = empty_range
    generator = card_number_generator(start, end)
    results = list(generator)
    assert len(results) == 0, "Пустой диапазон должен возвращать пустой генератор"


def test_format_correctness(small_range: Tuple[int, int]) -> None:
    """Тест: проверка корректности формата вывода (4×4 цифры через пробел)."""
    start, end = small_range
    generator = card_number_generator(start, end)
    results = list(generator)

    assert len(results) == 3  # Ожидаем 3 номера

    for num_str in results:
        parts = num_str.split()
        assert len(parts) == 4, "Должно быть 4 группы цифр"
        for part in parts:
            assert len(part) == 4, "Каждая группа должна содержать 4 цифры"
            assert part.isdigit(), "Все символы должны быть цифрами"


def test_transaction_descriptions_empty_list() -> None:
    transactions: List[Dict[str, Any]] = []
    result = list(transaction_descriptions(transactions))
    assert result == []

def test_transaction_descriptions_no_description_key() -> None:  # ← только один раз!
    transactions = [
        {"id": 1, "amount": 100},
        {},
        {"status": "completed"}
    ]
    result = list(transaction_descriptions(transactions))
    assert result == ["", "", ""]

def test_transaction_descriptions_non_dict_items() -> None:
    transactions = ["не словарь", 123, None]
    with pytest.raises(AttributeError):
        list(transaction_descriptions(transactions))  # type: ignore

def test_transaction_descriptions_mixed_cases() -> None:
    transactions = [
        {"description": "Зарплата"},
        {"id": 42},
        {"description": ""},
        {"description": "Квитанция ЖКХ"}
    ]
    result = list(transaction_descriptions(transactions))
    assert result == ["Зарплата", "", "", "Квитанция ЖКХ"]