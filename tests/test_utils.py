import unittest
from unittest.mock import patch, mock_open
import json

from src.utils import load_financial_operations


class TestMyClass(unittest.TestCase):

    def setUp(self):
        """Подготавливаем тестовые данные"""
        self.valid_data = [
            {"id": 1, "amount": 100.0, "currency": "RUB"},
            {"id": 2, "amount": 200.0, "currency": "USD"}
        ]
        self.invalid_json = '{"key": "value"'  # не список
        self.corrupted_json = '{"missing": "comma"}'  # синтаксическая ошибка

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_load_successful(self, mock_file_check, mock_file_opener):
        """Тест: успешная загрузка корректного JSON-файла с корневым массивом"""
        # Настраиваем мок для open() внутри теста
        mock_file_opener.return_value.read.return_value = json.dumps(self.valid_data)

        result = load_financial_operations("test.json")

        # Проверка результата
        self.assertEqual(result, self.valid_data)

        # Проверка вызовов моков
        mock_file_check.assert_called_with("test.json")
        mock_file_opener.assert_called_once()
        mock_file_opener.assert_called_with("test.json", "r", encoding="utf-8")

    @patch('os.path.isfile', return_value=False)
    def test_file_not_found(self, mock_isfile):
        """Тест: файл не существует → возвращаем пустой список"""
        result = load_financial_operations("nonexistent.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("nonexistent.json")

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_io_error_on_open(self, mock_open, mock_isfile):
        """Тест: ошибка чтения файла (IOError) → пустой список"""
        result = load_financial_operations("broken.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("broken.json")
        mock_open.assert_called_with("broken.json", "r", encoding="utf-8")

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_json_decode_error(self, mock_isfile, mock_open):
        """Тест: некорректный JSON → пустой список"""
        # Настраиваем мок внутри теста
        mock_open.return_value.read.return_value = self.corrupted_json

        result = load_financial_operations("corrupted.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("corrupted.json")
        mock_open.assert_called_with("corrupted.json", "r", encoding="utf-8")

    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_non_list_root(self, mock_isfile, mock_open):
        """Тест: JSON есть, но не список в корне → пустой список"""
        # Настраиваем мок внутри теста
        mock_open.return_value.read.return_value = self.invalid_json

        result = load_financial_operations("not_a_list.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("not_a_list.json")
        mock_open.assert_called_with("not_a_list.json", "r", encoding="utf-8")

    @patch('os.path.isfile', side_effect=OSError("Device not ready"))
    def test_os_error_on_isfile(self, mock_isfile):
        """Тест: ошибка при проверке существования файла (OSError) → пустой список"""
        result = load_financial_operations("os_error.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("os_error.json")


if __name__ == '__main__':
    unittest.main()
