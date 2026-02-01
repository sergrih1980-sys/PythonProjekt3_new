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
    @patch('builtins.open', mock_open())
    def test_load_successful(self, mock_isfile, mock_file):
        mock_isfile.return_value = True
        mock_file.return_value.read.return_value = json.dumps(self.valid_data)


        result = load_financial_operations("test.json")
        self.assertEqual(result, self.valid_data)
        mock_isfile.assert_called_with("test.json")
        mock_file.assert_called_with("test.json", "r", encoding="utf-8")

    @patch('os.path.isfile')
    def test_file_not_found(self, mock_isfile):
        mock_isfile.return_value = False
        result = load_financial_operations("nonexistent.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("nonexistent.json")

    @patch('os.path.isfile')
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    def test_io_error_on_open(self, mock_isfile, mock_open):
        mock_isfile.return_value = True
        result = load_financial_operations("broken.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("broken.json")

    @patch('os.path.isfile')
    @patch('builtins.open', mock_open())
    def test_json_decode_error(self, mock_isfile, mock_file):
        mock_isfile.return_value = True
        mock_file.return_value.read.return_value = self.corrupted_json

        result = load_financial_operations("corrupted.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("corrupted.json")
        mock_file.assert_called_with("corrupted.json", "r", encoding="utf-8")

    @patch('os.path.isfile')
    @patch('builtins.open', mock_open())
    def test_non_list_root(self, mock_isfile, mock_file):
        mock_isfile.return_value = True
        mock_file.return_value.read.return_value = self.invalid_json


        result = load_financial_operations("not_a_list.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("not_a_list.json")
        mock_file.assert_called_with("not_a_list.json", "r", encoding="utf-8")

    @patch('os.path.isfile', side_effect=OSError("Device not ready"))
    def test_os_error_on_isfile(self, mock_isfile):
        result = load_financial_operations("os_error.json")
        self.assertEqual(result, [])
        mock_isfile.assert_called_with("os_error.json")


if __name__ == '__main__':
    unittest.main()
