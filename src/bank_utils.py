import csv
import json
import re
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

""" Загрузка данных из разных форматов """


def load_from_json(filepath: str) -> List[Dict[str, Any]]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_from_csv(filepath: str) -> List[Dict[str, Any]]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def load_from_xlsx(filepath: str) -> List[Dict[str, Any]]:
    df = pd.read_excel(filepath)
    return df.to_dict('records')


#  Фильтрация и сортировка
def filter_by_status(data: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    target = status.strip().upper()
    valid_statuses = {'EXECUTED', 'CANCELED', 'PENDING'}
    if target not in valid_statuses:
        return []
    return [op for op in data if op.get('status', '').upper() == target]


def sort_by_date(data: List[Dict[str, Any]], ascending: bool = True) -> List[Dict[str, Any]]:
    return sorted(
        data,
        key=lambda x: x.get('date', ''),
        reverse=not ascending
    )


def filter_ruble_only(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        op for op in data
        if str(op.get('currency', '')).upper() in {'RUB', 'РУБ'}
    ]


# Поиск по описанию
def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    if not search or not data:
        return []
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [
        op for op in data
        if pattern.search(str(op.get('description', '')))
    ]


def format_date(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d.%m.%Y')
    except ValueError:
        return date_str


def print_operations(ops: List[Dict[str, Any]]):
    if not ops:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(ops)}")
    for op in ops:
        date = format_date(op.get('date', ''))
        desc = op.get('description', '')
        from_acc = op.get('from', '')
        to_acc = op.get('to', '')
        amount = op.get('amount', '')
        currency = op.get('currency', '')

        print(f"\n{date} {desc}")
        if from_acc:
            print(f"От: {from_acc}")
        if to_acc:
            print(f"Кому: {to_acc}")
        print(f"Сумма: {amount} {currency}")


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Группирует банковские операции по категориям и подсчитывает количество операций в каждой категории.

    Args:
        data: список словарей с полем 'description'
        categories: список названий категорий для поиска

    Returns:
        Словарь с количеством операций по каждой категории
    """
    result = {category: 0 for category in categories}

    for operation in data:
        # 1. Получаем описание, приводим к нижнему регистру
        description = operation.get('description', '').lower()

        # 2. Нормализуем разделители: заменяем тире, дефисы на пробелы
        for separator in ['—', '-', '–', '―', '−']:
            description = description.replace(separator, ' ')

        # 3. Убираем лишние пробелы (множественные пробелы → один пробел)
        description = ' '.join(description.split())

        # 4. Проверяем каждую категорию
        for category in categories:
            category_lower = category.lower()
            if category_lower in description:
                result[category] += 1

    return result