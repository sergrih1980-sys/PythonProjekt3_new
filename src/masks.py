import logging

# --- Настройка логера модуля 'masks' ---
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)  # Уровень не ниже DEBUG

# Форматировщик: метка времени | имя модуля | уровень | сообщение
file_formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# FileHandler: записывает в файл, перезаписывая его при каждом запуске
file_handler = logging.FileHandler('logs.log', mode='w', encoding='utf-8')
file_handler.setFormatter(file_formatter)

# Добавляем handler в логгер
if not logger.handlers:
    logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты, возвращает строку
    в формате: XXXX XX** **** XXXX"""
    logger.debug(f"Входные данные get_mask_card_number: '{card_number}'")

    # Удаляем все нецифровые символы
    digits = ''.join(filter(str.isdigit, card_number))
    logger.debug(f"Извлечены цифры: '{digits}'")

    # Если цифр нет — возвращаем шаблон с пробелами
    if not digits:
        logger.error("Номер карты не содержит цифр → возврат шаблона '    ** ****    '")
        return '    ** ****    '

    # Для номеров короче 12 цифр — особый формат
    if len(digits) < 12:
        logger.warning(f"Номер карты короткий ({len(digits)} цифр) → особый формат")
        prefix = digits[:4].ljust(4, ' ')
        result = f'{prefix} ** ****    '
        logger.debug(f"Результат (короткий): '{result}'")
        return result

    # Стандартный формат для 12+ цифр
    first_4 = digits[:4]
    middle_2 = digits[4:6]
    last_4 = digits[-4:]
    result = f'{first_4} {middle_2}** **** {last_4}'

    logger.info(f"Маска карты сформирована: '{result}'")
    return result


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.
    Возвращает строку в формате: **XXXX
    """
    logger.debug(f"Входные данные get_mask_account: '{account_number}'")

    # Извлекаем только цифры
    digits = ''.join(filter(str.isdigit, account_number))
    logger.debug(f"Извлечены цифры: '{digits}'")

    # Если цифр нет — просто возвращаем **
    if not digits:
        logger.error("Номер счёта не содержит цифр → возврат '**'")
        return '**'

    # Если цифр <= 4 — дополняем до 4 нулями слева
    if len(digits) <= 4:
        padded = digits.zfill(4)
        result = f'**{padded}'
        logger.info(f"Счёт дополнен до 4 цифр: '{result}'")
        return result

    # Иначе — берём последние 4 цифры
    result = f'**{digits[-4:]}'
    logger.info(f"Маска счёта сформирована: '{result}'")
    return result


if __name__ == "__main__":
    # Тестовые вызовы
    test_card_number = "7000 7922 8960 6361"
    print("Маска карты:", get_mask_card_number(test_card_number))

    test_account_number = "73654108430135874305"
    print("Маска счёта:", get_mask_account(test_account_number))

    # Тесты на ошибки
    print("Маска пустой карты:", get_mask_card_number(""))
    print("Маска пустого счёта:", get_mask_account(""))
