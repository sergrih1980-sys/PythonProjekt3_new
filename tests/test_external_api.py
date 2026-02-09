
from unittest.mock import MagicMock, patch

import requests

from src.external_api import currency_conversion

# Тестовые данные
TRANSACTION_RUB = {
    "operationAmount": {"amount": 1000.0, "currency": {"code": "RUB"}}
}

TRANSACTION_USD = {
    "operationAmount": {"amount": 100.0, "currency": {"code": "USD"}}
}

TRANSACTION_UNKNOWN = {
    "operationAmount": {"amount": 200.0, "currency": {"code": "GBP"}}
}

TRANSACTION_EMPTY = {}

TRANSACTION_MISSING_AMOUNT = {
    "operationAmount": {"currency": {"code": "USD"}}
}


def test_rub_no_conversion():
    """RUB → без конвертации"""
    result = currency_conversion(TRANSACTION_RUB)
    assert result == 1000.0


@patch('requests.get')
def test_usd_conversion_success(mock_get):
    """Успешная конвертация USD → RUB"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 9500.0}
    mock_get.return_value = mock_response

    result = currency_conversion(TRANSACTION_USD)

    assert result == 9500.0

    # Проверяем, что URL содержит from_=USD
    args, kwargs = mock_get.call_args
    assert "from_=USD" in args[0]
    assert "to=RUB" in args[0]
    assert "amount=100.0" in args[0]


def test_unknown_currency():
    """Неизвестная валюта → 0.0"""
    result = currency_conversion(TRANSACTION_UNKNOWN)
    assert result == 0.0


@patch('requests.get')
def test_empty_transaction(mock_get):
    """Пустой transaction → 0.0 (API не вызывается)"""
    result = currency_conversion(TRANSACTION_EMPTY)
    assert result == 0.0
    mock_get.assert_not_called()


@patch('requests.get')
def test_missing_amount(mock_get):
    """Нет amount → 0.0 (API не вызывается)"""
    result = currency_conversion(TRANSACTION_MISSING_AMOUNT)
    assert result == 0.0
    mock_get.assert_not_called()


@patch('requests.get', side_effect=requests.exceptions.RequestException("Network error"))
def test_request_exception(mock_get):
    """Ошибка сети → 0.0"""
    result = currency_conversion(TRANSACTION_USD)
    assert result == 0.0
