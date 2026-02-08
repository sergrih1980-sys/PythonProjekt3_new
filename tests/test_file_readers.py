import unittest
from unittest.mock import mock_open, patch
import pandas as pd
import os
from src.file_readers import read_transactions_csv, read_transactions_excel



class TestReadTransactionsExcel(unittest.TestCase):

    @patch('pandas.read_excel')
    @patch('os.path.exists', return_value=True)
    def test_read_excel_success(self, mock_read_excel, mock_exists):
        """Тест успешного чтения Excel-файла."""
        mock_df = pd.DataFrame([
            {'дата': '2024-01-01', 'сумма': 1000},
            {'дата': '2024-01-02', 'сумма': -500}
        ])
        mock_read_excel.return_value = mock_df

        result = read_transactions_excel('dummy.xlsx')

        expected = [
            {'дата': '2024-01-01', 'сумма': 1000},
            {'дата': '2024-01-02', 'сумма': -500}
        ]
        self.assertEqual(result, expected)

    @patch('os.path.exists', return_value=False)
    def test_file_not_found_excel(self, mock_exists):
        """Тест: Excel-файл не найден."""
        with self.assertRaises(FileNotFoundError) as context:
            read_transactions_excel('nonexistent.xlsx')
        self.assertIn('Файл не найден', str(context.exception))

    @patch('pandas.read_excel', side_effect=ValueError('Неверный формат Excel'))
    @patch('os.path.exists', return_value=True)
    def test_invalid_excel_format(self, mock_read_excel, mock_exists):
        """Тест: неверный формат Excel-файла."""
        with self.assertRaises(ValueError) as context:
            read_transactions_excel('invalid.xlsx')
        self.assertEqual(str(context.exception), 'Неверный формат Excel')

    @patch('pandas.read_excel', return_value=pd.DataFrame())
    @patch('os.path.exists', return_value=True)
    def test_empty_excel(self, mock_read_excel, mock_exists):
        """Тест: пустой Excel-файл."""
        result = read_transactions_excel('empty.xlsx')
        self.assertEqual(result, [])



class TestReadTransactionsCSV(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='дата,сумма\n2024-01-01,1000\n2024-01-02,-500')
    @patch('os.path.exists', return_value=True)
    def test_read_csv_success(self, mock_file, mock_exists):
        """Тест успешного чтения CSV-файла."""
        result = read_transactions_csv('dummy.csv')

        expected = [
            {'дата': '2024-01-01', 'сумма': '1000'},
            {'дата': '2024-01-02', 'сумма': '-500'}
        ]
        self.assertEqual(result, expected)

    @patch('os.path.exists', return_value=False)
    def test_file_not_found(self, mock_exists):
        """Тест: файл не найден."""
        with self.assertRaises(FileNotFoundError) as context:
            read_transactions_csv('nonexistent.csv')
        self.assertIn('Файл не найден', str(context.exception))

    @patch('builtins.open', side_effect=OSError('Ошибка чтения файла'))
    @patch('os.path.exists', return_value=True)
    def test_io_error_on_read(self, mock_file, mock_exists):
        """Тест: ошибка при чтении файла."""
        with self.assertRaises(OSError) as context:
            read_transactions_csv('broken.csv')
        self.assertEqual(str(context.exception), 'Ошибка чтения файла')


    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('os.path.exists', return_value=True)
    def test_empty_csv(self, mock_file, mock_exists):
        """Тест: пустой CSV-файл."""
        result = read_transactions_csv('empty.csv')
        self.assertEqual(result, [])
