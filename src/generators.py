from typing import Any, Dict, Generator, Iterator, List


def filter_by_currency(spisok: List[Dict[str, Any]], valuta: str) -> Iterator[Dict[str, Any]]:
    """
    Функция принимает список транзакций (словари) и код валюты,
    возвращает объект filter, содержащий только транзакции, где код валюты
    совпадает с заданным.
    """
    return filter(
        lambda x: x["operationAmount"]["currency"]["code"] == valuta,
        spisok
    )


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Генератор, возвращающий описания транзакций по очереди.
    """
    for transaction in transactions:
        description = transaction.get("description", "")
        # Приводим к строке, даже если это число/None/False
        yield str(description) if description is not None else ""


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
    """
    for num in range(start, end + 1):
        padded = str(num).zfill(16)
        yield f"{padded[:4]} {padded[4:8]} {padded[8:12]} {padded[12:16]}"
