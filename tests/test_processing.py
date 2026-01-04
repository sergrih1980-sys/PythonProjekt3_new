import pytest

from src.processing import filter_by_state, sort_by_date


def test_missing_state_key() -> None:
    """Тест: у некоторых словарей нет ключа 'state' — они игнорируются."""
    data = [
        {"id": "1", "state": "EXECUTED"},
        {"id": "2"},  # Нет ключа 'state'
        {"id": "3", "state": "EXECUTED"},
    ]
    result = filter_by_state(data, "EXECUTED")
    assert len(result) == 2
    assert all(item["id"] in ["1", "3"] for item in result)


def test_empty_list() -> None:
    """Тест: пустой входной список — возвращается пустой список."""
    result = filter_by_state([], "EXECUTED")
    assert result == []


@pytest.mark.parametrize("operations,state,expected_count", [
    # Сценарий 1: только EXECUTED
    ([{'state': 'EXECUTED'}, {'state': 'EXECUTED'}], 'EXECUTED', 2),
    # Сценарий 2: нет совпадений
    ([{'state': 'CANCELED'}], 'EXECUTED', 0),
    # Сценарий 3: смешанные статусы
    ([{'state': 'EXECUTED'}, {'state': 'CANCELED'}], 'CANCELED', 1),
])
def test_filter_by_state_parametrized(
    operations: list[dict[str, str]],
    state: str,
    expected_count: int
) -> None:
    result = filter_by_state(operations, state)
    assert len(result) == expected_count


@pytest.mark.parametrize("operations,reverse,expected_ids", [
    # Сценарий 1: убывание, 3 элемента
    ([
         {'id': 1, 'date': '2024-01-10'},
         {'id': 2, 'date': '2024-01-05'},
         {'id': 3, 'date': '2024-01-15'}
     ], True, [3, 1, 2]),
    # Сценарий 2: возрастание, 2 элемента
    ([
         {'id': 1, 'date': '2024-01-01'},
         {'id': 2, 'date': '2024-01-10'}
     ], False, [1, 2]),
    # Сценарий 3: одинаковые даты
    ([
         {'id': 1, 'date': '2024-01-05'},
         {'id': 2, 'date': '2024-01-05'}
     ], True, [1, 2]),
])
def test_sort_by_date_parametrized(
    operations: list[dict[str, Any]],
    reverse: bool,
    expected_ids: list[int]
) -> None:
    result = sort_by_date(operations, reverse)
    assert [item['id'] for item in result] == expected_ids


def test_sort_by_date_empty_list() -> None:
    result = sort_by_date([], reverse=True)
    assert result == []  # Должен вернуться пустой список


def test_sort_by_date_single_item() -> None:
    operations = [{'id': 1, 'date': '2024-01-10'}]
    result = sort_by_date(operations, reverse=False)
    assert result[0]['id'] == 1


def test_missing_date_key() -> None:
    """Тест: отсутствует ключ 'date' — должно вызвать KeyError."""
    data = [{"value": "NoDate"}]
    with pytest.raises(KeyError):
        sort_by_date(data, reverse=True)
