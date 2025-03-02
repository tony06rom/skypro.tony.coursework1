import datetime
import json
import os
from pathlib import Path

from src.logger import get_logger
from src.reports import spending_by_category
from src.services import cashback_category
from src.utils import excel_reader
from src.views import main_page

ROOT_DIR = Path(__file__).resolve().parents[0]
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"

logger = get_logger("logger", f"{LOGS_DIR}\\{os.path.basename(os.path.abspath(__file__))}.log")


def main(date: datetime.datetime | str):
    """Основная функция программы получающая на вход текущую дату и выполняющая команды пользователя"""
    data = excel_reader(f"{DATA_DIR}\\operations.xlsx")
    logger.info("DataFrame с банковскими операциями успешно прочитан")

    print("# Доступные команды:\n - main_page\n - cashback\n - report")

    logger.info("Запрос команды у пользователя")
    user_input = input("Введите команду:\n===> ")

    if user_input == "main_page":
        logger.info("Выбрана функция views.main_page")
        print("Ознакомьтесь с ответом:\n")
        print(json.loads(main_page(date)))

    if user_input == "cashback":
        logger.info("Выбрана функция services.cashback")
        print("# Период за которые необходимо вывести категории выгодного кэшбэка")
        month = int(input("# Месяц [**]:\n===> "))
        year = int(input("# Год [****]:\n===> "))
        print("Ознакомьтесь с ответом:\n")
        print(json.loads(cashback_category(data, year, month)))

    if user_input == "report":
        logger.info("Выбрана функция reports.spending_by_category")
        print("# Введите данные для получения списка трат за три месяца до указанной даты")
        category = input("# Категория [Фастфуд]:\n===> ")
        date = input("# Дата [**.**.****]:\n===> ")
        print("Ознакомьтесь с ответом:\n")
        spending_by_category(data, category, date)


if __name__ == "__main__":
    #today = datetime.datetime.today()  # На сегодняшний день. Подойдет для
    today = datetime.datetime.today() - datetime.timedelta(days=1825)  # Если бы "сегодня" было 5 лет назад.
    # Подойдет для cards и top_transactions
    print(f"Дата на сегодня: {today}")
    main(today)

    logger.info("Программа успешно завершила работу")
