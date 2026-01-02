def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты, возвращает строку
    в формате: XXXX XX** **** XXXX"""
    # Удаляем все нецифровые символы
    digits = ''.join(filter(str.isdigit, card_number))

    # Если цифр нет - возвращаем шаблон с пробелами
    if not digits:
        return '    ** ****    '

    # Для номеров короче 12 цифр - особый формат
    if len(digits) < 12:
        # Берём до 4 первых цифр, дополняем пробелами
        prefix = digits[:4].ljust(4, ' ')
        return f'{prefix} ** ****    '

    # Стандартный формат для 12+ цифр: XXXX XX** **** XXXX
    first_4 = digits[:4]
    middle_2 = digits[4:6]
    last_4 = digits[-4:]

    return f'{first_4} {middle_2}** **** {last_4}'


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.
    Возвращает строку в формате: **XXXX
    """
    # Извлекаем только цифры
    digits = ''.join(filter(str.isdigit, account_number))

    # Если цифр нет - просто возвращаем **
    if not digits:
        return '**'

    # Если цифр <= 4 - дополняем до 4 нулями слева
    if len(digits) <= 4:
        padded = digits.zfill(4)
        return f'**{padded}'

    # Иначе - берём последние 4 цифры
    return f'**{digits[-4:]}'


if __name__ == "__main__":
    test_card_number = "7000 7922 8960 6361"
    print(get_mask_card_number(test_card_number))

    test_account_number = "73654108430135874305"
    print(get_mask_account(test_account_number))
