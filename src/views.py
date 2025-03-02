import datetime
import json
import os
from pathlib import Path

import pandas as pd

from src.logger import get_logger
from src.utils import excel_reader, get_currency_rates, get_stock_prices

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"
CONF_DIR = ROOT_DIR / "configs"

logger = get_logger("logger", f"{LOGS_DIR}\\{os.path.basename(os.path.abspath(__file__))}.log")


def cards_collector(data: pd.DataFrame) -> list:
    """ Принимает список банковских операций и возвращает сумму трат по картам """
    data = data.to_dict("records")
    cards_data = {}
    result = []

    def get_last_digits(operation):
        """ Фильтрация операций """
        return type(operation.get("Номер карты")) is str

    filtered_data = filter(get_last_digits, data)

    for row in filtered_data:
        if cards_data.get(row.get("Номер карты")) is None:
            cards_data[row.get("Номер карты")] = {
                "last_digits": row.get("Номер карты")[1:],
                "total_spent": 0.0,
                "cashback": 0,
            }
        if float(row.get("Сумма операции")) < 0:
            cards_data[row.get("Номер карты")]["total_spent"] += abs(float(row.get("Сумма операции")))
        if row.get("Кэшбэк") is not None and row.get("Кэшбэк") > 0:
            logger.debug(f"cashback: {row.get('Кэшбэк')}")
            cards_data[row.get("Номер карты")]["cashback"] += abs(int(row.get("Кэшбэк")))

    for card in cards_data.values():
        card["total_spent"] = round(card.get("total_spent"), 2)
        card["cashback"] = int(card.get("cashback") // 100)
        result.append(card)

    return result


def top_transactions(data: pd.DataFrame) -> list:
    """Принимает список банковских операций и возвращает топ-5 транзакций по сумме платежа"""
    data = data.to_dict("records")
    sorted_transactions = sorted(
        data,
        key=lambda operation: (
            operation.get("Сумма операции"),
            datetime.datetime.strptime(operation.get("Дата операции"), "%d.%m.%Y %H:%M:%S"),
        ),
        reverse=True,
    )
    top = []
    for transaction in sorted_transactions[:5]:
        top.append(
            (
                {
                    "amount": transaction.get("Сумма операции"),
                    "category": transaction.get("Категория"),
                    "date": transaction.get("Дата операции")[:10],
                    "description": transaction.get("Описание"),
                }
            )
        )
    return top


def currency_rates(currency_list) -> list:
    """Возвращает стоимость валют из заданного списка через API"""
    return get_currency_rates(currency_list)


def main_page(date: datetime) -> json:
    """Принимает на вход текущую дату и возвращает JSON с расходами и кэшбэком по каждой карте, топ-5 транзакций
    по сумме платежа, курс валют и стоимость акций указанных в файле user_settings.json"""
    greeting = ""
    if 4 > date.hour < 10:
        greeting = "Доброе утро"
    elif 10 >= date.hour < 17:
        greeting = "Добрый день"
    elif 17 >= date.hour < 23:
        greeting = "Добрый вечер"
    elif 23 >= date.hour < 24 or 0 < date.hour < 4:
        greeting = "Доброй ночи"

    month_start = datetime.datetime(date.year, date.month, 1)

    data = excel_reader(f"{DATA_DIR}\\operations.xlsx")
    data = data.to_dict("records")

    filtered_data = []

    for line in data:
        if date >= datetime.datetime.strptime(line.get("Дата операции"), "%d.%m.%Y %H:%M:%S") >= month_start:
            filtered_data.append(line)

    with open(f"{CONF_DIR}\\user_settings.json") as json_file:
        user_settings = json.load(json_file)

    filtered_data = pd.DataFrame(filtered_data)
    print(type(filtered_data))

    result = {
        "greeting": greeting,
        "cards": cards_collector(filtered_data),
        "top_transactions": top_transactions(filtered_data),
        "currency_rates": get_currency_rates(user_settings.get("user_currencies")),
        "stock_prices": get_stock_prices(user_settings.get("user_stocks")),
    }

    return json.dumps(result)
