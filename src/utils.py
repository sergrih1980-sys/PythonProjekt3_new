import json
import os
from typing import List, Dict, Any


def load_financial_operations(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: Список транзакций или пустой список при ошибках.
    """
    if not os.path.isfile(file_path):
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        else:
            return []

    except (json.JSONDecodeError, IOError, OSError):
        return []
