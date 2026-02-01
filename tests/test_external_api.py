import unittest
from unittest.mock import patch, MagicMock
import requests
from src.external_api import currency_conversion

class TestCurrencyConversion(unittest.TestCase):

    def setUp(self):
        """Подготавливаем тестовые данные"""
        self.transaction_usd = {
            "operationAmount": {
                "amount": 50.0,
                "currency": {"code": "USD"}
            }
        }
        self.transaction_eur = {
            "operationAmount": {
                "amount": 30.0,
                "currency": {"code": "EUR"}
            }
        }
        self.transaction_gbp = {  # Неподдерживаемая валюта
            "operationAmount": {
                "amount": 200.0,
                "currency": {"code": "GBP"}
            }
        }

        # Моки для ответов API
        self.mock_success = MagicMock()
        self.mock_success.status_code = 200
        self.mock_success.json.return_value = {"result": 4850.5}

    @patch('src.external_api.currency_converter.requests.get', return_value=self.mock_success)
    def test_usd_conversion_success(self, mock_get):
        """USD → успешный ответ API, возвращаем result"""
        result = currency_conversion(self.transaction_usd)
        self.assertEqual(result, 4850.5)
        mock_get.assert_called_once()

        expected_url = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=50.0"
        mock_get.assert_called_with(expected_url, headers={"apikey": "mocked_api_key"})

    @patch('src.external_api.currency_converter.requests.get', return_value=self.mock_success)
    def test_eur_conversion_success(self, mock_get):
        """EUR → успешный ответ API, возвращаем result"""
        result = currency_conversion(self.transaction_eur)
        self.assertEqual(result, self.mock_success.json.return_value["result"])
        mock_get.assert_called_once()

    @patch('src.external_api.currency_converter.requests.get')
    def test_unsupported_currency_returns_zero(self, mock_get):
        """Неподдерживаемая валюта (GBP) → 0.0, API не вызывается"""
        result = currency_conversion(self.transaction_gbp)
        self.assertEqual(result, 0.0)
        mock_get.assert_not_called()

    @patch('src.external_api.currency_converter.requests.get')
    def test_api_request_exception_returns_zero(self, mock_get):
        """Исключение при запросе → 0.0"""
        mock_get.side_effect = requests.exceptions.RequestException("Connection failed")
        result = currency_conversion(self.transaction_usd)
        self.assertEqual(result, 0.0)
        mock_get.assert_called_once()

if __name__ == '__main__':
    unittest.main()