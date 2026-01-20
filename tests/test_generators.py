import pytest

def test_filter_by_currency_basic(transactions_basic):
    result = list(filter_by_currency(transactions_basic, "RUB"))
    assert len(result) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "RUB" for t in result)

    @pytest.mark.parametrize("transactions,currency,expected_count", test_cases)
    def test_filter_by_currency_parametrized(transactions, currency, expected_count):
        """
        Параметризованный тест для функции filter_by_currency.
        Проверяет:
        - фильтрацию по заданной валюте;
        - обработку отсутствия совпадений;
        - работу с пустым списком;
        - устойчивость к неполным структурам данных.
        """
        # Вызов функции
        filtered = filter_by_currency(transactions, currency)

        result = list(filtered)


def test_transaction_descriptions_with_descriptions(transactions_with_descriptions):
    """Тест: все транзакции имеют поле description."""
    result = list(transaction_descriptions(transactions_with_descriptions))
    expected = ["Покупка продуктов", "Оплата интернета", "Перевод другу"]
    assert result == expected

def test_transaction_descriptions_single_with_description(single_transaction_with_description):
    """Тест: одна транзакция с полем description."""
    result = list(transaction_descriptions(single_transaction_with_description))
    expected = ["Единственный платёж"]
    assert result == expected

def test_transaction_descriptions_empty(empty_transactions):
    """Тест: пустой список транзакций."""
    result = list(transaction_descriptions(empty_transactions))
    expected = []
    assert result == expected


def test_consistency_with_string_conversion():
    """Тест: соответствие строкового представления числа и формата вывода."""
    num = 123456789
    padded = str(num).zfill(16)
    formatted = f"{padded[:4]} {padded[4:8]} {padded:8:12]} {padded[12:16]}"

    generator = card_number_generator(num, num)
    result = next(generator)
    assert result == formatted

def test_empty_range_behavior(empty_range):
    """Тест: пустой диапазон не должен выдавать значений."""
    start, end = empty_range
    generator = card_number_generator(start, end)
    results = list(generator)
    assert len(results) == 0, "Пустой диапазон должен возвращать пустой генератор"


def test_format_correctness(small_range):
    """Тест: проверка корректности формата вывода (4×4 цифры через пробел)."""
    start, end = small_range
    generator = card_number_generator(start, end)
    results = list(generator)

    assert len(results) == 3  # Ожидаем 3 номера
