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
        self.invalid_json = '{"key": "value"}'  # не список
        self.corrupted_json = '{"missing": "comma"}'  # синтаксическая ошибка


    @patch('os.path.isfile')
    @patch('builtins.open', mock_open(read_data=json.dumps(self.valid_data)))
    def test_load_successful(self, mock_isfile, mock_file):
        """Тест: успешная загрузка корректного JSON-файла с корневым массивом"""
        mock_isfile.return_value = True


        result = load_financial_operations("test.json")

        self.assertEqual(result, self.valid_data)
        mock_isfile.assert_called_with("test.json")
        mock_file.assert_called_with("test.json", "r", encoding="utf-8")

    @patch('os.path.isfile')
    def test_file_not_found(self, mock_isfile):
        """Тест: файл не существует → возвращаем пустой список"""
        mock_isfile.return_value = False

        result = load_financial_operations("nonexistent.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("nonexistent.json")


    @patch('os.path.isfile')
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_io_error_on_open(self, mock_isfile, mock_open):
        """Тест: ошибка чтения файла (IOError) → пустой список"""
        mock_isfile.return_value = True


        result = load_financial_operations("broken.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("broken.json")

    @patch('os.path.isfile')
    @patch('builtins.open', mock_open(read_data=self.corrupted_json))
    def test_json_decode_error(self, mock_isfile, mock_file):
        """Тест: некорректный JSON → пустой список"""
        mock_isfile.return_value = True

        result = load_financial_operations("corrupted.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("corrupted.json")
        mock_file.assert_called_with("corrupted.json", "r", encoding="utf-8")

    @patch('os.path.isfile')
    @patch('builtins.open', mock_open(read_data=self.invalid_json))
    def test_non_list_root(self, mock_isfile, mock_file):
        """Тест: JSON есть, но не список в корне → пустой список"""
        mock_isfile.return_value = True

        result = load_financial_operations("not_a_list.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("not_a_list.json")
        mock_file.assert_called_with("not_a_list.json", "r", encoding="utf-8")


    @patch('os.path.isfile', side_effect=OSError("Device not ready"))
    def test_os_error_on_isfile(self, mock_isfile):
        """Тест: ошибка при проверке существования файла (OSError) → пустой список"""
        result = load_financial_operations("os_error.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("os_error.json")

if __name__ == '__main__':
    unittest.main()
