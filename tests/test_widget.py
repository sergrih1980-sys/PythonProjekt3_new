import pytest
from src.widget import mask_account_card, get_date


# --- Тесты для mask_account_card ---

@pytest.mark.parametrize("input_data, error_msg", [
    ("", "Введите корректный номер Вашей карты или счёта"),
    ("Visa 1234", "Введите корректный номер Вашей карты или счёта"),  # <16 цифр
    ("Счет 123", "Введите корректный номер Вашей карты или счёта"),     # <20 цифр
    ("Unknown 12345678901234567890", "Введите корректный номер Вашей карты или счёта"),  # 20 цифр, но не 'счет'
    ("Card ", "Введите корректный номер Вашей карты или счёта"),         # нет цифр
    ("Счет ABC", "Введите корректный номер Вашей карты или счёта"),   # нет цифр в счете
])
def test_mask_account_card_invalid(input_data, error_msg) -> None:
    """Тестируем некорректные/граничные входные данные."""
    result = mask_account_card(input_data)
    assert result == error_msg


@pytest.mark.parametrize("input_data, expected_prefix", [
    ("МИР 2200111122223333", "МИР 2200 11** **** 3333"),
    ("Tinkoff Black 5555666677778888", "Tinkoff Black 5555 66** **** 8888"),
])
def test_mask_account_card_other_card_types(input_data, expected_prefix) -> None:
    """Тестируем другие типы карт (МИР, Tinkoff и т.п.)."""
    result = mask_account_card(input_data)
    assert result == expected_prefix


# --- Тесты для get_date ---

@pytest.mark.parametrize("date_string, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2000-01-01T00:00:00.000000", "01.01.2000"),
    ("2025-12-31T23:59:59.999999", "31.12.2025"),
    # Без миллисекунд
    ("2023-05-15T10:15:20", "15.05.2023"),
])
def test_get_date_valid(date_string, expected) -> None:
    """Тестируем корректный формат даты."""
    result = get_date(date_string)
    assert result == expected


@pytest.mark.parametrize("date_string, error_msg", [
    ("", "Некорректный формат даты"),
    ("2024-03-11", "Некорректный формат даты"),           # нет 'T'
    ("11-03-2024T02:26:18", "Некорректный формат даты"),  # неверный порядок
    ("invalid-date", "Некорректный формат даты"),
    ("2024-13-01T00:00:00", "Некорректный формат даты"),  # неверный месяц
    ("2024-00-10T00:00:00", "Некорректный формат даты"),  # неверный день
    ("2024-02-30T00:00:00", "Некорректный формат даты"),  # 30 февраля
    ("abc", "Некорректный формат даты"),
    (None, "Некорректный формат даты"),                    # None
    (123, "Некорректный формат даты"),                     # не строка
])
def test_get_date_invalid(date_string, error_msg) -> None:
    """Тестируем некорректные/граничные входные данные."""
    result = get_date(date_string)
    assert result == error_msg


@pytest.mark.parametrize("date_string, expected", [
    ("2024/03/11T02:26:18", "Некорректный формат даты"),
    ("2024.03.11T02:26:18", "Некорректный формат даты"),
])
def test_get_date_wrong_separators(date_string, expected) -> None:
    """Тестируем неверные разделители в дате."""
    result = get_date(date_string)
    assert result == expected
