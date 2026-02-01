import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = "https://api.exchangeratesapi.com/v1/latest"

def currency_conversion(transaction: dict) -> float:
    """ Конвертируем валюту через API и возвращаем его """
    amount = transaction.get("operationAmount", {}).get("amount")
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")

    if currency == "RUB":
        return amount
    elif currency in ["USD", "EUR"]:
        try:
            response = requests.get(
                API_URL.format(to="RUB", from_="currency", amount=amount), headers={"apiky": API_KEY}
            )
            if response.status_code ==200:
                data = response.json()
                return data["result"]
            else:
                print(f"Ошибка при конвертации валюты: {response.status_code}")
                return 0.0
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при конвертации валюты: {e}")
            return 0.0
    else:
        return 0.0





