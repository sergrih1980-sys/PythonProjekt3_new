import os
import json


def load_financial_operations(filepath):
    """
    Загружает финансовые операции из JSON-файла.

    Args:
        filepath (str): путь к JSON-файлу

    Returns:
        list: список словарей с операциями. Если файл:
            - не найден → []
            - пуст → []
            - содержит не-список → []
            - некорректный JSON → []
    """
    # Проверяем существование файла
    if not os.path.isfile(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Проверяем, что данные — список
        if isinstance(data, list):
            return data
        else:
            return []  # Не список — возвращаем пустой список

    except (OSError, IOError, json.JSONDecodeError):
        # Ошибки: нет доступа, повреждённый файл, синтаксис JSON
        return []
