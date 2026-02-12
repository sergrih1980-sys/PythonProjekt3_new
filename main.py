
from typing import List, Dict

from src.generators import filter_by_currency
from src.masks import get_mask_account, get_mask_card_number
from src.utils import load_financial_operations
from src.widget import get_date, mask_account_card


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

# Импорты локальных функций
from src.bank_utils import process_bank_search
from src.file_readers import read_transactions_csv, read_transactions_excel
from src.processing import filter_by_state, sort_by_date


def main(операций=None, transaction=None):
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON‑файла")
    print("2. Получить информацию о транзакциях из CSV‑файла")
    print("3. Получить информацию о транзакциях из XLSX‑файла")

    # Выбор источника данных
    while True:
        choice = input("> ").strip()
        if choice in ['1', '2', '3']:
            break
        print("Некорректный выбор. Введите 1, 2 или 3.")

    file_path = input("Введите путь к файлу: ").strip()

    # Загрузка данных в зависимости от выбора
    try:
        if choice == '1':
            print("Для обработки выбран JSON‑файл.")
            transactions = load_financial_operations(file_path)
        elif choice == '2':
            print("Для обработки выбран CSV‑файл.")
            transactions = read_transactions_csv(file_path)
        elif choice == '3':
            print("Для обработки выбран XLSX‑файл.")
            transactions = read_transactions_excel(file_path)
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return

    if not transactions:
        print("Не удалось загрузить транзакции. Проверьте путь к файлу и его содержимое.")
        return

    # Фильтрация по статусу (с приведением к верхнему регистру)
    valid_states = {'EXECUTED', 'CANCELED', 'PENDING'}
    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

    while True:
        status = input("> ").strip().upper()
        if status in valid_states:
            break
        print(f'Статус операции "{status}" недоступен.')
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")


    filtered_transactions = filter_by_state(transactions, status)
    print(f'Операции отфильтрованы по статусу "{status}".')


    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # Сортировка по дате
    print("Отсортировать операции по дате? Да/Нет")
    sort_choice = input("> ").strip().lower()
    if sort_choice in ['да', 'yes', 'y']:
        print("Отсортировать по возрастанию или по убыванию?")
        order_choice = input("> ").strip().lower()
        reverse = order_choice in ['убыванию', 'desc', 'убыв']
        filtered_transactions = sort_by_date(filtered_transactions, reverse)

    # Фильтрация по валюте (только RUB)
    print("Выводить только рублёвые транзакции? Да/Нет")
    rub_choice = input("> ").strip().lower()
    if rub_choice in ['да', 'yes', 'y']:
        try:
            filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))
        except KeyError:
            print("В данных отсутствует поле 'operationAmount.currency.code'. Пропускаем фильтрацию по валюте.")
        if not filtered_transactions:
            print("Не найдено ни одной рублёвой транзакции.")
            return

    # Поиск по описанию (регулярное выражение)
    print("Отфильтровать список транзакций по определённому слову в описании? Да/Нет")
    search_choice = input("> ").strip().lower()
    if search_choice in ['да', 'yes', 'y']:
        search_term = input("Введите слово/шаблон для поиска в описании: ").strip()
        if search_term:
            try:
                filtered_transactions = process_bank_search(filtered_transactions, search_term)
            except ValueError as e:
                print(f"Ошибка в регулярном выражении: {e}")
                return
            if not filtered_transactions:
                print("Не найдено транзакций, соответствующих поисковому запросу.")
                return

    # Вывод итогового результата
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"!Всего банковских операций в выборке: {len(filtered_transactions)}\n")

    for idx, transaction in enumerate(filtered_transactions, 1):
        # Извлекаем и форматируем данные
        date_str = transaction.get('date', 'Неизвестно')
        description = transaction.get('description', 'Нет описания')
        amount = transaction.get('amount', 'Неизвестно')
        currency = transaction.get('currency', 'Неизвестно')


        # Форматируем дату (если ISO-формат)
        if isinstance(date_str, str) and 'T' in date_str:
            date_str = date_str.split('T')[0]  # Берём только дату

        print(f"{idx}. {date_str} {description}")
        print(f"!   Сумма: {amount} {currency}")
        print()



if __name__ == "__main__":
    main()