def filter_by_currency(spisok, valuta):

  """
    Функция принимает список транзакций (словари) и код валюты,
    возвращает объект filter, содержащий только транзакции, где код валюты
    совпадает с заданным.
   """
  return filter(
        lambda x: x["operationAmount"]["currency"]["code"] == valuta,
        spisok
    )


def transaction_descriptions(transactions):
    """
    Генератор, возвращающий описания транзакций по очереди.
    """
    for transaction in transactions:
        # Безопасное получение описания: если ключа нет — возвращаем пустую строку
        description = transaction.get('description', '')
        yield description


def card_number_generator(start, end):
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
    """
    for num in range(start, end + 1):
        # Формируем 16‑значный номер с нулями слева
        padded = str(num).zfill(16)
        # Разбиваем на группы по 4 цифры
        yield f"{padded[:4]} {padded[4:8]} {padded[8:12]} {padded[12:16]}"





