from typing import Dict, List


from src.masks import get_mask_account, get_mask_card_number
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

    ''' Теперь executed_transactions гарантированно список (возможно, пустой) '''

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

        ''' Примеры использования (можно убрать в продакшене)'''
    if __name__ == "__main__":
        ''' Тестирование маскирования карт/счетов '''
        print(mask_account_card("Visa Platinum 7000792289606361"))  # 7000 79** **** 6361
        print(mask_account_card("Maestro 7000792289606361"))  # 7000 79** **** 6361
        print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305

        ''' Тестирование преобразования даты '''
        print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
        print(get_date("2025-12-20T10:30:45.123456"))  # 20.12.2025
        print(get_date("некорректная_дата")) # Неверный формат даты

