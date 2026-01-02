import pytest
from src.masks import get_mask_card_number, get_mask_account



class TestMaskingFunctions:

    @pytest.mark.parametrize(
        "input_card, expected_output",
        [
            ("1234567890123456", "1234 56** **** 3456"),
            ("1234 5678 9012 3456", "1234 56** **** 3456"),
            ("123456789012", "1234 56** **** 012"),
            ("12345678901234567890", "1234 56** **** 7890"),
            ("", "     ** ****    "),
            ("1", "1   ** ****    "),
            ("1234", "1234 ** ****    "),
        ]
    )
    def test_get_mask_card_number(self, input_card, expected_output):
        """Тестирует маскировку номера карты."""
        result = get_mask_card_number(input_card)
        assert result == expected_output

    @pytest.mark.parametrize(
        "input_account, expected_output",
        [
            ("1234567890", "**7890"),
            ("1234", "**1234"),
            ("123", "**123"),
            ("", "**"),
            ("1", "**1"),
            ("abc1234", "**234"),  # нецифровые символы
            ("0000", "**0000"),
        ]
    )
    def test_get_mask_account(self, input_account, expected_output):
        """Тестирует маскировку номера счёта."""
        result = get_mask_account(input_account)
        assert result == expected_output