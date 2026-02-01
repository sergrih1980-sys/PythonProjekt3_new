import unittest
from unittest.mock import patch, MagicMock
from external_api.currency_converter import currency_conversion


class TestCurrencyConversion(unittest.TestCase):

    def setUp(self):
        """Подготавливаем тестовые данные"""
        self.transaction_rub = {
            "operationAmount": {
                "amount": 1000.0,
                "currency": {"code": "RUB"}
            }
        }
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
        self.missing_amount = {  # Нет amount
            "operationAmount": {
                "currency": {"code": "USD"}
            }
        }
        self.missing_currency = {  # Нет currency
            "operationAmount": {
                "amount": 100.0
            }
        }
        self.no_operation_amount = {}  # Нет operationAmount

    @patch('your_module.external_api.currency_converter.requests.get')
    def test_rub_returns_amount(self, mock_get):
        """RUB → возвращаем исходную сумму, API не вызывается"""
        result = currency_conversion(self.transaction_rub)
        self.assertEqual(result, 1000.0)
        mock_get.assert_not_called()

    @patch('your_module.external_api.currency_converter.requests.get')
    def test_usd_conversion_success(self, mock_get):
        """USD → успешный ответ API, возвращаем result"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 4850.5}
        mock_get.return_value = mock_response

        result = currency_conversion(self.transaction_usd)
        self.assertEqual(result, 4850.5)
        mock_get.assert_called_once()

    @patch('your_module.external_api.currency_converter.requests.get')
    def test_eur_conversion_success(self, mock_get):
        """EUR → успешный ответ API, возвращаем result"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 3240.3}
        mock_get.return_value = mock_response

        result = currency_conversion(self.transaction_eur)
        self.assertEqual(result, 3240.3)
        mock_get.assert_called_once()

    @patch('your_module.external_api.currency_converter.requests.get')
    def test_unsupported_currency_returns_zero(self, mock_get):
        """Неподдерживаемая валюта (GBP) → 0.0, API не вызывается"""
        result = currency_conversion(self.transaction_gbp)
        self.assertEqual(result, 0.0)
        mock_get.assert_not_called()