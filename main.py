from src.bank_utils import process_bank_search
from src.masks import get_mask_account, get_mask_card_number
from src.widget import get_date, mask_account_card
from typing import List, Dict, Any


def filter_by_state(
        dict_list: List[Dict[str, str]],
        state: str = "EXECUTED"
) -> List[Dict[str, str]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Returns:
        Список словарей (может быть пустым, но не None).
    """
    filtered_list = []
    for item in dict_list:
        if item.get('state') == state:
            filtered_list.append(item)
    return filtered_list  # Всегда возвращает список!


def sort_by_date(
        list_dict: List[Dict[str, str]],
        reverse: bool = True
) -> List[Dict[str, str]]:
    """
    Сортирует список словарей по дате (ключу 'date').
    """
    return sorted(list_dict, key=lambda x: x["date"], reverse=reverse)


if __name__ == "__main__":
    test_data = [
        {'id': '41428829', 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': '939719570', 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': '594226727', 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': '615064591', 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

    executed_transactions = filter_by_state(test_data, "EXECUTED")
    # Теперь executed_transactions гарантированно список (возможно, пустой)

    if executed_transactions:  # Проверяем, есть ли данные
        sorted_transactions = sort_by_date(executed_transactions, reverse=True)
        print("Отфильтрованные и отсортированные транзакции:")
        for transaction in sorted_transactions:
            print(transaction)
    else:
        print("Нет транзакций в статусе 'EXECUTED'")

    if __name__ == "__main__":
        test_card_number = "7000 7922 8960 6361"
        print(get_mask_card_number(test_card_number))

        test_account_number = "73654108430135874305"
        print(get_mask_account(test_account_number))

        # Примеры использования (можно убрать в продакшене)
    if __name__ == "__main__":
        # Тестирование маскирования карт/счетов
        print(mask_account_card("Visa Platinum 7000792289606361"))  # 7000 79** **** 6361
        print(mask_account_card("Maestro 7000792289606361"))  # 7000 79** **** 6361
        print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305

        # Тестирование преобразования даты
        print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
        print(get_date("2025-12-20T10:30:45.123456"))  # 20.12.2025
        print(get_date("некорректная_дата"))  # Некорректный формат даты


import json
import csv
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any


def load_data(filepath: str, file_type: str) -> List[Dict[str, Any]]:
    """Загружает данные из файла указанного типа."""
    if file_type == 'json':
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif file_type == 'csv':
        with open(filepath, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    elif file_type == 'xlsx':
        df = pd.read_excel(filepath)
        return df.to_dict('records')
    else:
        raise ValueError("Неподдерживаемый формат файла")

def format_date(date_str: str) -> str:
    """Преобразует строку даты в формат ДД.ММ.ГГГГ."""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d.%m.%Y')
    except:
        return date_str

def print_operations(ops: List[Dict[str, Any]]):
    """Выводит операции в читаемом формате."""
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

def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")


    # Выбор источника данных
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("> ").strip()
    data: List[Dict[str, Any]] = []

    if choice == '1':
        filepath = input("Введите путь к JSON-файлу: ").strip()
        data = load_data(filepath, 'json')
        print("Для обработки выбран JSON-файл.")
    elif choice == '2':
        filepath = input("Введите путь к CSV-файлу: ").strip()
        data = load_data(filepath, 'csv')
        print("Для обработки выбран CSV-файл.")
    elif choice == '3':
        filepath = input("Введите путь к XLSX-файлу: ").strip()
        data = load_data(filepath, 'xlsx')
        print("Для обработки выбран XLSX-файл.")
    else:
        print("Неверный выбор. Завершаем работу.")
        return

    # Фильтрация по статусу
    valid_statuses = {'EXECUTED', 'CANCELED', 'PENDING'}
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input("> ").strip().upper()
        if status in valid_statuses:
            filtered = [op for op in data if op.get('status', '').upper() == status]
            print(f'Операции отфильтрованы по статусу "{status}"')
            break
        else:
            print(f'Статус операции "{status}" недоступен.')

    # Сортировка по дате
    print("Отсортировать операции по дате? Да/Нет")
    sort_choice = input("> ").strip().lower()
    if sort_choice in ('да', 'yes', 'y'):
        print("Отсортировать по возрастанию или по убыванию?")
        order = input("> ").strip().lower()
        ascending = order in ('возрастанию', 'asc', 'по возрастанию')
        filtered.sort(key=lambda x: x.get('date', ''), reverse=not ascending)

    # Фильтрация рублёвых операций
    print("Выводить только рублевые транзакции? Да/Нет")
    ruble_choice = input("> ").strip().lower()
    if ruble_choice in ('да', 'yes', 'y'):
        filtered = [
            op for op in filtered
            if str(op.get('currency', '')).upper() in {'RUB', 'РУБ'}
        ]

    # Поиск по слову в описании
    print("Отфильтровать список транзакций по определённому слову в описании? Да/Нет")
    search_choice = input("> ").strip().lower()
    if search_choice in ('да', 'yes', 'y'):
        search_word = input("Введите слово для поиска: ").strip()
        filtered = process_bank_search(filtered, search_word)

    # Вывод результата
    print("Распечатываю итоговый список транзакций...")
    print_operations(filtered)

if __name__ == '__main__':
    main()