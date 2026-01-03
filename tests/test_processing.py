import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize("operations,state,expected_count", [
    # Сценарий 1: только EXECUTED
    ([{'state': 'EXECUTED'}, {'state': 'EXECUTED'}], 'EXECUTED', 2),
    # Сценарий 2: нет совпадений
    ([{'state': 'CANCELED'}], 'EXECUTED', 0),
    # Сценарий 3: смешанные статусы
    ([{'state': 'EXECUTED'}, {'state': 'CANCELED'}], 'CANCELED', 1),
])
def test_filter_by_state_parametrized(operations, state, expected_count):
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
def test_sort_by_date_parametrized(operations, reverse, expected_ids):
    result = sort_by_date(operations, reverse)
    assert [item['id'] for item in result] == expected_ids


def test_sort_by_date_empty_list():
    result = sort_by_date([], reverse=True)
    assert result == []  # Должен вернуться пустой список

def test_sort_by_date_single_item():
        operations = [{'id': 1, 'date': '2024-01-10'}]
        result = sort_by_date(operations, reverse=False)
        assert result[0]['id'] == 1