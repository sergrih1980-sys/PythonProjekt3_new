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