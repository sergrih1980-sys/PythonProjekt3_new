import json
import unittest
from unittest.mock import mock_open, patch

from src.utils import load_financial_operations


class TestLoadFinancialOperations(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.valid_data = [
            {"id": 1, "amount": 100.0, "currency": "RUB"},
            {"id": 2, "amount": 200.0, "currency": "USD"}
        ]
        self.invalid_json = '{"key": "value"}'           # JSON, но не список
        self.corrupted_json = '{"missing": "comma"'     # синтаксическая ошибка
        self.empty_content = ''                        # пустой файл

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_successful(self, mock_file, mock_isfile):
        """Успешная загрузка корректного JSON-файла"""
        mock_isfile.return_value = True
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(self.valid_data)

        result = load_financial_operations("test.json")

        self.assertEqual(result, self.valid_data)
        mock_isfile.assert_called_with("test.json")
        mock_file.assert_called_with("test.json", "r", encoding="utf-8")

    @patch('os.path.isfile')
    def test_file_not_found(self, mock_isfile):
        """Файл не существует"""
        mock_isfile.return_value = False

        result = load_financial_operations("nonexistent.json")

        self.assertEqual(result, [])
        mock_isfile.assert_called_with("nonexistent.json")

    @patch('os.path.isfile')
    @patch('builtins.open')
    def test_io_error_on_open(self, mock_file, mock_isfile):
        """Ошибка при открытии файла (например, нет прав доступа)"""
        mock_isfile.return_value = True
        mock_file.side_effect = IOError("Permission denied")

        result = load_financial_operations("broken.json")

        self.assertEqual(result, [])
        mock_isfile.assert_called_with("broken.json")
        mock_file.assert_called_with("broken.json", "r", encoding="utf-8")

    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=mock_open)
    def test_json_decode_error(self, mock_file, mock_isfile):
        """Некорректный JSON (синтаксическая ошибка)"""
        mock_isfile.return_value = True
        mock_file.return_value.__enter__.return_value.read.return_value = self.corrupted_json

        result = load_financial_operations("corrupted.json")

        self.assertEqual(result, [])
        mock_isfile.assert_called_with("corrupted.json")
        mock_file.assert_called_with("corrupted.json", "r", encoding="utf-8")
