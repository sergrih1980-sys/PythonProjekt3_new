from masks import get_mask_account, get_mask_card_number


def mask_account_card(user_number: str) -> str:
    """
    Принимает строку с типом и номером карты/счёта и возвращает маску.

    Примеры входных данных:
    - 'Visa Platinum 7000792289606361'
    - 'Maestro 7000792289606361'
    - 'Счет 73654108430135874305'

    Возвращает:
    - для карт: '7000 79** **** 6361'
    - для счетов: 'Счет **4305'
    """
    # Извлекаем только цифры из строки
    digits = ''.join(char for char in user_number if char.isdigit())
    count_code = len(digits)

    # Проверяем корректность длины номера
    if count_code not in (16, 20):
        return "Введите корректный номер Вашей карты или счёта"

    # Определяем тип продукта (карта или счёт)
    user_number_lower = user_number.lower()
    if 'счет' in user_number_lower or 'account' in user_number_lower:
        # Для счёта показываем только последние 4 цифры с префиксом **
        masked = f"**{digits[-4:]}"
        return f"Счет {masked}"
    else:
        # Для карт показываем первые 6 цифр, затем 6 звёздочек, затем последние 4
        masked = f"{digits[:6]}******{digits[-4:]}"
        # Форматируем в группы по 4 символа через пробел
        formatted = ' '.join(masked[i:i + 4] for i in range(0, len(masked), 4))
        return formatted


def get_date(date_string: str) -> str:
    """
    Принимает строку с датой в формате 'YYYY-MM-DDTHH:MM:SS.ffffff'
    и возвращает дату в формате 'ДД.ММ.ГГГГ'.

    Пример:
        Вход:  '2024-03-11T02:26:18.671407'
        Выход: '11.03.2024'
    """
    try:
        # Разделяем дату и время по символу 'T'
        date_part = date_string.split('T')[0]

        # Разбиваем дату на компоненты: год, месяц, день
        year, month, day = date_part.split('-')

        # Формируем итоговую строку в формате ДД.ММ.ГГГГ
        return f"{day}.{month}.{year}"

    except (ValueError, IndexError) as e:
        return "Некорректный формат даты"


# Примеры использования (можно убрать в продакшене)
if __name__ == "__main__":
    # Тестирование маскирования карт/счетов
    print(mask_account_card("Visa Platinum 7000792289606361"))  # 7000 79** **** 6361
    print(mask_account_card("Maestro 7000792289606361"))  # 7000 79** **** 6361
    print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305

    # Тестирование преобразования даты
    print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
    print(get_date("2025-12-20T10:30:45.123456"))  # 20.12.2025
    print(get_date("некорректная_дата"))  # Некорректный формат даты

result = get_mask_card_number("Visa 1234567890123456")
print(result)

test_account_number = "73654108430135874305"
print(get_mask_account(test_account_number))


