import csv
import json
import os
import unittest
from unittest.mock import patch
from src.bank_utils import process_bank_operations
import pandas as pd

# Импортируем тестируемые функции
from src.bank_utils import (filter_by_status, filter_ruble_only, load_from_csv, load_from_json, load_from_xlsx,
                            print_operations, process_bank_search)


class TestBankOperations(unittest.TestCase):

    # Вспомогательные данные для тестов
    SAMPLE_DATA = [
        {
            "date": "2023-01-15",
            "description": "Покупка в магазине Пятерочка",
            "status": "EXECUTED",
            "amount": 1250,
            "currency": "RUB",
            "from": "Счет **1111",
            "to": "Магазин 'Пятерочка'"
        },
        {
            "date": "2023-02-20",
            "description": "Перевод зарплаты",
            "status": "CANCELED",
            "amount": 50000,
            "currency": "RUB",
            "from": "Работодатель",
            "to": "Счет **2222"
        },
        {
            "date": "2023-03-10",
            "description": "Оплата интернета",
            "status": "PENDING",
            "amount": 850,
            "currency": "USD",
            "from": "Карта **3333",
            "to": "ISP Inc."
        }
    ]

    def setUp(self):
        """Подготовка временных файлов для тестов."""
        # JSON
        with open('test_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.SAMPLE_DATA, f, ensure_ascii=False, indent=2)
        # CSV
        with open('test_data.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.SAMPLE_DATA[0].keys())
            writer.writeheader()
            writer.writerows(self.SAMPLE_DATA)
        # XLSX
        df = pd.DataFrame(self.SAMPLE_DATA)
        df.to_excel('test_data.xlsx', index=False)

    def tearDown(self):
        """Удаление временных файлов после тестов."""
        for fname in ['test_data.json', 'test_data.csv', 'test_data.xlsx']:
            if os.path.exists(fname):
                os.remove(fname)

        # Тесты загрузки данных
    def test_load_from_json(self):
        data = load_from_json('test_data.json')
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['description'], 'Покупка в магазине Пятерочка')

    def test_load_from_csv(self):
        data = load_from_csv('test_data.csv')
        self.assertEqual(len(data), 3)
        self.assertEqual(data[1]['status'], 'CANCELED')

    @patch('pandas.read_excel')
    def test_load_from_xlsx(self, mock_read_excel):
        mock_read_excel.return_value = pd.DataFrame(self.SAMPLE_DATA)
        data = load_from_xlsx('dummy.xlsx')
        self.assertEqual(len(data), 3)
        self.assertEqual(data[2]['currency'], 'USD')

    def test_filter_by_status_invalid(self):
        filtered = filter_by_status(self.SAMPLE_DATA, 'INVALID')
        self.assertEqual(filtered, [])

        # Тест фильтрации рублёвых операций

    def test_filter_ruble_only(self):
        ruble_ops = filter_ruble_only(self.SAMPLE_DATA)
        self.assertEqual(len(ruble_ops), 2)  # Только RUB
        currencies = {op['currency'] for op in ruble_ops}
        self.assertTrue(all(curr in {'RUB', 'РУБ'} for curr in currencies))

    def test_process_bank_search_not_found(self):
        found = process_bank_search(self.SAMPLE_DATA, 'Магнит')
        self.assertEqual(found, [])

        # Тест вывода операций
    @patch('builtins.print')
    def test_print_operations_non_empty(self, mock_print):
        print_operations(self.SAMPLE_DATA[:1])
        output = ''.join(call[0][0] for call in mock_print.call_args_list)
        self.assertIn('Всего банковских операций в выборке: 1', output)
        self.assertIn('Покупка в магазине Пятерочка', output)

    @patch('builtins.print')
    def test_print_operations_empty(self, mock_print):
        print_operations([])
        mock_print.assert_called_with("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


class TestProcessBankOperations(unittest.TestCase):

    def test_basic_matching(self):
        """Тест: обычные совпадения категорий в описаниях."""
        data = [
            {'description': 'Покупка продуктов в магазине "Перекрёсток"'},
            {'description': 'Оплата интернета от провайдера Ростелеком'},
            {'description': 'Супермаркет "Азбука вкуса" — продукты'},
            {'description': 'Мобильная связь: пополнение счёта МТС'},
        ]
        categories = ['продукты', 'связь', 'интернет']

        result = process_bank_operations(data, categories)

        # Проверяем подсчёты
        self.assertEqual(result['продукты'], 2)
        self.assertEqual(result['связь'], 1)
        self.assertEqual(result['интернет'], 1)

    def test_no_matches(self):
        """Тест: ни одна категория не найдена в описаниях."""
        data = [
            {'description': 'Перевод на счёт в другом банке'},
            {'description': 'Комиссия за обслуживание карты'},
            {'description': 'Возврат товара в магазин одежды'},
        ]
        categories = ['продукты', 'транспорт', 'кафе']

        result = process_bank_operations(data, categories)

        # Все категории должны быть с нулём
        for category in categories:
            self.assertEqual(result[category], 0)

    def test_empty_inputs(self):
        """Тест: пустые входные данные."""
        # 1. Пустой список операций
        data_empty = []
        categories = ['продукты', 'связь']
        result1 = process_bank_operations(data_empty, categories)
        self.assertEqual(result1, {'продукты': 0, 'связь': 0})

        # 2. Пустой список категорий
        data = [{'description': 'Покупка продуктов'}]
        categories_empty = []
        result2 = process_bank_operations(data, categories_empty)
        self.assertEqual(result2, {})  # Ожидаем пустой словарь

        # 3. И операции, и категории пустые
        result3 = process_bank_operations([], [])
        self.assertEqual(result3, {})


if __name__ == '__main__':
    unittest.main()
