from src.masks import get_mask_account, get_mask_card_number
from datetime import datetime


def mask_account_card(user_number: str) -> str:
    """
    Принимает строку с типом и номером карты/счёта и возвращает маску.

    Примеры входных данных:
    - 'Visa Platinum 7000792289606361'
    - 'Maestro 7000792289606361'
    - 'Счет 73654108430135874305'

    Возвращает:
    - для карт: 'Visa Platinum 7000 79** **** 6361'
    - для счетов: 'Счет **4305'
    """
    # 1. Проверка типа и пустоты
    if not isinstance(user_number, str) or not user_number.strip():
        return "Введите корректный номер Вашей карты или счёта"

    user_number = user_number.strip()

    # 2. Извлекаем только цифры
    digits = ''.join(char for char in user_number if char.isdigit())
    count_code = len(digits)

    # 3. Проверяем длину номера
    if count_code not in (16, 20):
        return "Введите корректный номер Вашей карты или счёта"

    # 4. Определяем тип продукта
    user_number_lower = user_number.lower()

    if 'счет' in user_number_lower or 'account' in user_number_lower:
        # Для счёта: ** + последние 4 цифры
        masked = f"**{digits[-4:]}"
        return f"Счет {masked}"

    else:
        # Для карт: ищем позицию начала цифр
        num_start = None
        for i, char in enumerate(user_number):
            if char.isdigit():
                num_start = i
                break

        if num_start is None:
            return "Введите корректный номер Вашей карты или счёта"

        # Название карты — всё до номера
        card_name = user_number[:num_start].strip()

        # Формируем маску: первые 6 + 6 звёздочек + последние 4
        if count_code == 16:
            masked_number = f"{digits[:6]}******{digits[-4:]}"
        else:
            # Если вдруг 20 цифр, но не счёт (ошибка)
            return "Введите корректный номер Вашей карты или счёта"

        # Разбиваем на группы по 4 через пробел
        formatted_number = ' '.join(
            masked_number[i:i + 4] for i in range(0, len(masked_number), 4)
        )

        return f"{card_name} {formatted_number}"


def get_date(date_string: str) -> str:
    if not isinstance(date_string, str) or not date_string.strip():
        return "Некорректный формат даты"

    date_string = date_string.strip()

    if 'T' not in date_string:
        return "Некорректный формат даты"

    try:
        date_part = date_string.split('T')[0]

        # Эта строка вызовет ValueError, если дата некорректна
        datetime.strptime(date_part, "%Y-%m-%d")

        year, month, day = date_part.split('-')

        # Дополнительно проверяем, что все части — цифры и нужной длины
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            return "Некорректный формат даты"
        if len(year) != 4 or len(month) != 2 or len(day) != 2:
            return "Некорректный формат даты"

        return f"{day}.{month}.{year}"

    except (ValueError, AttributeError, IndexError):
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
