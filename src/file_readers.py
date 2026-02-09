import csv
import os

import pandas as pd


def read_transactions_csv(file_path):
    """
    Считывает финансовые операции из CSV‑файла.

    Args:
        file_path (str): путь к CSV‑файлу.


    Returns:
        list[dict]: список словарей, где каждый словарь — транзакция.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    transactions = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(dict(row))  # Преобразуем OrderedDict в обычный dict
    return transactions


def read_transactions_excel(file_path):
    """
    Считывает финансовые операции из Excel‑файла (.xlsx).

    Args:
        file_path (str): путь к Excel‑файлу.


    Returns:
        list[dict]: список словарей, где каждый словарь — транзакция.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    # Читаем Excel, предполагаем, что данные на первом листе
    df = pd.read_excel(file_path, engine='openpyxl')

    # Преобразуем DataFrame в список словарей
    transactions = df.to_dict(orient='records')
    return transactions
