
import os
from src.bank_utils import process_bank_search
from src.file_readers import read_transactions_csv, read_transactions_excel
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import load_financial_operations


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON‑файла")
    print("2. Получить информацию о транзакциях из CSV‑файла")
    print("3. Получить информацию о транзакциях из XLSX‑файла")

    # Выбор источника данных
    while True:
        choice = input("> ").strip()
        if choice in ['1', '2', '3']:
            break
        print("Некорректный выбор. Введите 1, 2 или 3.")

    file_path = input("Введите путь к файлу: ").strip()

    # Загрузка данных в зависимости от выбора
    try:
        if choice == '1':
            print("Для обработки выбран JSON‑файл.")
            transactions = load_financial_operations(file_path)
        elif choice == '2':
            print("Для обработки выбран CSV‑файл.")
            transactions = read_transactions_csv(file_path)
        elif choice == '3':
            print("Для обработки выбран XLSX‑файл.")
            transactions = read_transactions_excel(file_path)
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return

    if not transactions:
        print("Не удалось загрузить транзакции. Проверьте путь к файлу и его содержимое.")
        return

    # Фильтрация по статусу
    valid_states = {'EXECUTED', 'CANCELED', 'PENDING'}
    print("Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING")

    while True:
        status = input("Введите статус: ").strip().upper()
        if status in valid_states:
            break
        print(f'Статус операции "{status}" недоступен. Попробуйте ещё раз.')


    filtered_transactions = filter_by_state(transactions, status)
    print(f'Операции отфильтрованы по статусу "{status}".')


    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # Сортировка по дате
    print("Отсортировать операции по дате? (Да/Нет)")
    sort_choice = input("> ").strip().lower()
    if sort_choice in ['да', 'yes', 'y']:
        print("Отсортировать по возрастанию или по убыванию?")
        order_choice = input("> ").strip().lower()
        reverse = order_choice in ['убыванию', 'desc', 'убыв']
        filtered_transactions = sort_by_date(filtered_transactions, reverse)

    # Фильтрация по валюте (только RUB)
    print("Выводить только рублёвые транзакции? (Да/Нет)")
    rub_choice = input("> ").strip().lower()
    if rub_choice in ['да', 'yes', 'y']:
        try:
            filtered_transactions = list(filter_by_currency(filtered_transactions, "RUB"))
        except KeyError:
            print(
                "В данных отсутствует поле 'operationAmount.currency.code'. "
                "Пропускаем фильтрацию по валюте."
            )
        if not filtered_transactions:
            print("Не найдено ни одной рублёвой транзакции.")
            return

    # Поиск по описанию (регулярное выражение)
    print("Отфильтровать список транзакций по слову в описании? (Да/Нет)")
    search_choice = input("> ").strip().lower()
    if search_choice in ['да', 'yes', 'y']:
        search_term = input("Введите слово/шаблон для поиска: ").strip()
        if search_term:  # Проверка на пустую строку
            try:
                filtered_transactions = process_bank_search(
                    filtered_transactions, search_term
                )
            except ValueError as e:
                print(f"Ошибка в регулярном выражении: {e}. Пример: '.*магазин.*'")
                return
            if not filtered_transactions:
                print("Не найдено транзакций, соответствующих поисковому запросу.")
                return

    # Вывод итогового результата
    print("\n" + "=" * 60)  # Убран лишний "!"
    print(f"Итого найдено транзакций: {len(filtered_transactions)}")
    if rub_choice in ['да', 'yes', 'y']:
        print("Фильтр: только RUB")
    if search_term:
        print(f"Поиск: '{search_term}'")
    print("=" * 60 + "\n")

    for idx, transaction in enumerate(filtered_transactions, 1):
        date_str = transaction.get('date', 'Неизвестно') or 'Неизвестно'
        description = transaction.get('description', 'Нет описания') or 'Нет описания'
        amount = transaction.get('amount') or 'Неизвестно'
        currency = transaction.get('currency') or 'Неизвестно'

        # Безопасная обработка даты
        if isinstance(date_str, str):
            if 'T' in date_str:
                date_str = date_str.split('T')[0]  # ISO формат
            elif '.' in date_str and len(date_str.split('.')) == 3:
                pass  # оставляем DD.MM.YYYY
            else:
                date_str = 'Неизвестно'

        print(f"{idx}. {date_str} | {description}")
        print(f"   Сумма: {amount} {currency}")
        print("-" * 50)

# Тестовый блок
if __name__ == "__main__":
    main()