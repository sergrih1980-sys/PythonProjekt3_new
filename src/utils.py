import json
import logging
import os
from typing import Any, Dict, List

# --- Настройка логера модуля 'utils' ---
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)  # Уровень не ниже DEBUG

# Форматировщик: время | модуль | уровень | сообщение
file_formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# FileHandler: перезаписывает файл при каждом запуске
file_handler = logging.FileHandler('logs.log', mode='w', encoding='utf-8')
file_handler.setFormatter(file_formatter)

# Добавляем handler, если его ещё нет
if not logger.handlers:
    logger.addHandler(file_handler)


def load_financial_operations(filepath: str) -> List[Dict[str, Any]]:
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
    logger.debug(f"Попытка загрузить операции из файла: '{filepath}'")

    # Проверяем существование файла
    if not os.path.isfile(filepath):
        logger.error(f"Файл не найден: '{filepath}' → возврат пустого списка")
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Проверяем, что данные — список
        if isinstance(data, list):
            logger.info(f"Файл '{filepath}' успешно загружен. Найдено {len(data)} операций")
            return data
        else:
            logger.error(f"Данные в файле '{filepath}' не являются списком → возврат пустого списка")
            return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка синтаксиса JSON в файле '{filepath}': {e} → возврат пустого списка")
        return []

    except (OSError, IOError) as e:
        logger.error(f"Ошибка чтения файла '{filepath}': {e} → возврат пустого списка")
        return []


if __name__ == "__main__":
    # Тестовые вызовы
    operations = load_financial_operations("operations.json")
    print("Загруженные операции:", operations)

    # Тест на несуществующий файл
    operations_missing = load_financial_operations("non_existent.json")
    print("Операции из несуществующего файла:", operations_missing)
