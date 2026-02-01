import os

import requests
from dotenv import load_dotenv

API_KEY = os.getenv("API_KEY")
API_URL = "https://api.apilayer.com/exchangerates_data/convert?to={to}&from_={from_}&amount={amount}"

load_dotenv()


def currency_conversion(transaction: dict) -> float:
    amount = transaction.get("operationAmount", {}).get("amount")
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if currency == "RUB":
        return amount if amount is not None else 0.0  # Защита от None

    elif currency in ["USD", "EUR"]:
        # Ключевая проверка: если amount отсутствует → возвращаем 0.0
        if amount is None:
            return 0.0

        try:
            url = API_URL.format(to="RUB", from_=currency, amount=amount)
            response = requests.get(url, headers={"apikey": API_KEY})

            if response.status_code == 200:
                data = response.json()
                return data["result"]
            else:
                print(f"Ошибка при конвертации валюты: {response.status_code} {response.text}")
                return 0.0
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при конвертации валюты: {e}")
            return 0.0
    else:
        return 0.0
