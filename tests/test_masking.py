import pytest
from src.masks import get_mask_card_number, get_mask_account



def test_get_mask_card_number_long():
    # Стандартная 16‑значная карта
    result = get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"

def test_get_mask_card_number_short():
    # Короткая карта (8 цифр)
    result = get_mask_card_number("12345678")
    assert result == "1234 ** ****    "

def test_get_mask_card_number_empty():
    # Пустая строка
    result = get_mask_card_number("")
    assert result == "    ** ****    "

def test_get_mask_account_short():
    # 3 цифры
    result = get_mask_account("abc123")
    assert result == "**0123"

def test_get_mask_account_long():
    # Больше 4 цифр
    result = get_mask_account("abc12345678")
    assert result == "**5678"

def test_get_mask_account_empty():
    # Пустой ввод
    result = get_mask_account("")
    assert result == "**"