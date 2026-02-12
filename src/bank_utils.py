import re
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет операции, в описании которых содержится заданная строка (с поддержкой регулярных выражений).

    Параметры:
        data: список словарей с операциями (ожидается поле 'description' типа str)
        search: строка поиска (регулярное выражение)

    Возвращает:
        Список словарей с подходящими операциями
    """
    try:
        pattern = re.compile(search, re.IGNORECASE)
    except re.error as e:
        raise ValueError(f"Ошибка в регулярном выражении: {e}")

    return [
        op for op in data
        if ('description' in op and
            isinstance(op['description'], str) and
            pattern.search(op['description']))
    ]


def process_bank_operations(
        data: List[Dict[str, Any]],
        categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.

    Категория определяется по наличию подстроки из списка categories
    в поле 'description' (без учёта регистра).

    Параметры:
        data: список словарей с операциями
        categories: список названий категорий для поиска

    Возвращает:
        Словарь вида {категория: количество_операций}
    """
    result = {category: 0 for category in categories}

    for operation in data:
        if ('description' not in operation or
                not isinstance(operation['description'], str)):
            continue

        desc_lower = operation['description'].lower()

        for category in categories:
            if category.lower() in desc_lower:
                result[category] += 1

    return result
