import pytest
from typing import List, Dict, Any
from src.bank_utils import process_bank_search, process_bank_operations


# Тестовые данные
TEST_DATA = [
    {"id": 1, "description": "Покупка продуктов в магазине Пятёрочка"},
    {"id": 2, "description": "Оплата интернета МТС"},
    {"id": 3, "description": "Перевод другу на карту"},
    {"id": 4, "description": "Снятие наличных в банкомате"},
    {"id": 5, "description": "Возврат средств за товар"},
    # Операция без поля description
    {"id": 6},
    # description не строка
    {"id": 7, "description": 123},
]

class TestProcessBankSearch:
    def test_find_exact_match(self):
        """Поиск по точной подстроке."""
        result = process_bank_search(TEST_DATA, "Пятёрочка")
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_case_insensitive(self):
        """Регистронезависимый поиск."""
        result = process_bank_search(TEST_DATA, "мтс")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_regex_simple(self):
        """Поиск с простым регулярным выражением."""
        result = process_bank_search(TEST_DATA, r"Перевод.*карту")
        assert len(result) == 1
        assert result[0]["id"] == 3

    def test_regex_or_condition(self):
        """Регулярное выражение с альтернативой (OR)."""
        result = process_bank_search(TEST_DATA, r"Пятёрочка|МТС")
        assert len(result) == 2
        assert {op["id"] for op in result} == {1, 2}

    def test_no_matches(self):
        """Нет совпадений — возвращается пустой список."""
        result = process_bank_search(TEST_DATA, "Кофе")
        assert result == []

    def test_invalid_regex(self):
        """Некорректное регулярное выражение вызывает ValueError."""
        with pytest.raises(ValueError, match="Ошибка в регулярном выражении"):
            process_bank_search(TEST_DATA, r"[")

class TestProcessBankOperations:
    def test_exact_category_match(self):
        """Точное совпадение категории."""
        categories = ["Покупка", "Перевод"]
        result = process_bank_operations(TEST_DATA, categories)
        assert result["Покупка"] == 1  # "Покупка продуктов..."
        assert result["Перевод"] == 1   # "Перевод другу..."

    def test_case_insensitive_category(self):
        """Поиск категорий без учёта регистра."""
        categories = ["мтс", "ПЯТЁРОЧКА"]
        result = process_bank_operations(TEST_DATA, categories)
        assert result["мтс"] == 1
        assert result["ПЯТЁРОЧКА"] == 1

    def test_partial_match_in_description(self):
        """Частичное совпадение подстроки в описании."""
        categories = ["наличн", "возврат"]
        result = process_bank_operations(TEST_DATA, categories)
        assert result["наличн"] == 1  # "Снятие наличных..."
        assert result["возврат"] == 1   # "Возврат средств..."


    def test_category_not_found(self):
        """Категория не найдена — счётчик 0."""
        categories = ["Кофе", "Аптека"]
        result = process_bank_operations(TEST_DATA, categories)
        assert result["Кофе"] == 0
        assert result["Аптека"] == 0

    def test_empty_data(self):
        """Пустой список операций — все категории имеют 0."""
        categories = ["Покупка", "Перевод"]
        result = process_bank_operations([], categories)
        assert result["Покупка"] == 0
        assert result["Перевод"] == 0

    def test_no_description_field(self):
        """Операция без 'description' — пропускается."""
        data = [{"id": 1}, {"id": 2, "description": "Покупка"}]
        categories = ["Покупка"]
        result = process_bank_operations(data, categories)
        assert result["Покупка"] == 1

    def test_description_not_string(self):
        """'description' не строка — пропускается."""
        data = [
            {"id": 1, "description": "Покупка"},
            {"id": 2, "description": 456}
        ]
        categories = ["Покупка"]
        result = process_bank_operations(data, categories)
        assert result["Покупка"] == 1

    def test_multiple_matches_one_operation(self):
        """Одна операция подходит под несколько категорий."""
        data = [{"description": "Перевод и покупка одновременно"}]
        categories = ["Перевод", "Покупка"]
        result = process_bank_operations(data, categories)
        assert result["Перевод"] == 1
        assert result["Покупка"] == 1

    def test_empty_categories(self):
        """Пустой список категорий — возвращается пустой словарь."""
        result = process_bank_operations(TEST_DATA, [])
        assert result == {}

