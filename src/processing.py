from typing import List, Dict

def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Фильтрует список транзакций по указанному состоянию.

    Args:
        transactions: Список словарей с данными транзакций.
        state: Строка с состоянием транзакции (по умолчанию "EXECUTED").

    Returns:
        Список транзакций, соответствующих указанному состоянию.
    """
    filtered_transactions = []
    for transaction in transactions:
        if transaction['state'] == state:
            filtered_transactions.append(transaction)
    return filtered_transactions



def sort_by_date(list_dict: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Сортирует список словарей по дате.

    Args:
        list_dict: Список словарей, содержащих поле 'date' в формате ISO.
        reverse: Флаг сортировки (True — по убыванию, False — по возрастанию).

    Returns:
        Отсортированный список словарей.
    """
    return sorted(list_dict, key=lambda x: x["date"], reverse=reverse)



# Пример данных
transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

# Фильтрация транзакций со статусом "EXECUTED"
executed_transactions = filter_by_state(transactions, "EXECUTED")

# Сортировка отфильтрованных транзакций по дате (по убыванию)
sorted_transactions = sort_by_date(executed_transactions, reverse=True)

print("Отфильтрованные и отсортированные транзакции:")
for transaction in sorted_transactions:
    print(transaction)