import pytest
from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number_long(self):
    # Стандартная 16‑значная карта
    result = get_mask_card_number("1234567890123456")
    self.assertEqual(result, "1234 56** **** 3456")

    # С пробелами
    result = get_mask_card_number("1234 5678 9012 3456")
    self.assertEqual(result, "1234 56** **** 3456")

    @pytest.mark.parametrize([
        ("1234567890123456", "1234 56** **** 3456"),
        ("1234 5678 9012 3456", "1234 56** **** 3456"),
        ("12345678", "1234 ** ****    "),
        ("1234", "1234 ** ****    "),
        ("", "    ** ****    "),
        ("  1234  5678  ", "1234 ** ****    "),
    ])
    def test_get_mask_card_number(self, card_number, expected):
        result = get_mask_card_number(card_number)
        self.assertEqual(result, expected)

    @pytest.mark.parametrize([
        ("abc123", "**0123"),
        ("1234", "**1234"),
        ("abc12345678", "**5678"),
        ("", "**"),
        ("x1y2z3", "**0023"),
        ("9", "**0009"),
    ])
    def test_get_mask_account(self, account_number, expected):
        result = get_mask_account(account_number)
        self.assertEqual(result, expected)