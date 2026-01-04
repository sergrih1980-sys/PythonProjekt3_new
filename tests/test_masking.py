
from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number_long() -> None:

    # Стандартная 16‑значная карта
    result = get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"


def test_get_mask_card_number_short() -> None:

    # Короткая карта (8 цифр)
    result = get_mask_card_number("12345678")
    assert result == "1234 ** ****    "


def test_get_mask_card_number_empty() -> None:

    # Пустая строка
    result = get_mask_card_number("")
    assert result == "    ** ****    "


def test_get_mask_account_short() -> None:

    # 3 цифры
    result = get_mask_account("abc123")
    assert result == "**0123"


def test_get_mask_account_long() -> None:

    # Больше 4 цифр
    result = get_mask_account("abc12345678")
    assert result == "**5678"


def test_get_mask_account_empty(account_empty: str) -> None:

    # Пустой ввод
    result = get_mask_account("")
    assert result == account_empty


def test_no_digits_in_input() -> None:
    """Во входной строке нет цифр."""
    assert get_mask_account("abc") == "**"
    assert get_mask_account("!@#$%") == "**"
    assert get_mask_account("") == "**"


def test_whitespace_and_symbols(symbol: str) -> None:
    """Строка с пробелами, дефисами и др. символами."""
    assert get_mask_account("  12-34-56  ") == symbol
    assert get_mask_account("\t\n789\r") == "**0789"  # visible_digits=4
