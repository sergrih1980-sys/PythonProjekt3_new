
def filter_by_currency(spisok, valuta):
    """
    Фильтрует список транзакций по указанной валюте.

    Функция принимает список транзакций (словари) и код валюты,
    возвращает объект filter, содержащий только транзакции, где код валюты
    совпадает с заданным.

    """

    return filter(
        lambda x: x["operationAmount"]["currency"]["code"] == valuta,
        spisok
    )






