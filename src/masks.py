def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты, возвращает строку
    в формате: XXXX XX** **** XXXX"""
    cleaned = card_number.replace(' ', '')
    if not cleaned:
        return '    ** ****    '
    if len(cleaned) < 12:
        prefix = cleaned.ljust(4, ' ')
        return f'{prefix} ** ****    '
    return f'{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}'


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.
    Возвращает строку в формате: **XXXX
    """
    # Извлекаем только цифры из входной строки
    digits = ''.join(filter(str.isdigit, account_number))

    # Если цифр ≤ 4 — возвращаем все цифры с префиксом **
    if len(digits) <= 4:
        return f'**{digits}'

    # Иначе — только последние 4 цифры с префиксом **
    return f'**{digits[-4:]}


if __name__ == "__main__":
    test_card_number = "7000 7922 8960 6361"
    print(get_mask_card_number(test_card_number))

    test_account_number = "73654108430135874305"
    print(get_mask_account(test_account_number))
