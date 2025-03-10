from datetime import datetime
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
    """Принимает список банковских операций и возвращает сумму трат по картам"""
    data_records = data.to_dict("records")
    cards_data = {}
    result = []

    def get_last_digits(operation: dict) -> bool:
        """Фильтрация операций"""
        return isinstance(operation["Номер карты"], str)

    filtered_data = list(filter(get_last_digits, data_records))

    for row in filtered_data:
        card_number = row["Номер карты"]

        if card_number not in cards_data:
            cards_data[card_number] = {
                "last_digits": card_number[1:],  # Используем срез строки
                "total_spent": 0.0,
                "cashback": 0,
            }

        amount = row.get("Сумма операции")
        if amount is not None:
            cards_data[card_number]["total_spent"] += abs(float(amount))

        cashback = row.get("Кэшбэк")
        if cashback is not None and cashback > 0:
            logger.debug(f"cashback: {cashback}")
            cards_data[card_number]["cashback"] += abs(int(cashback))

    for card in cards_data.values():
        card["total_spent"] = round(card["total_spent"], 2)
        card["cashback"] = int(card["cashback"] // 100)
        result.append(card)

    return result


def top_transactions(data: pd.DataFrame) -> list:
    """Принимает список банковских операций и возвращает топ-5 транзакций по сумме платежа"""
    data_records = data.to_dict("records")

    sorted_transactions = sorted(
        data_records,
        key=lambda operation: (
            operation["Сумма операции"],
            datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S"),
        ),
        reverse=True,
    )

    top = []
    for transaction in sorted_transactions[:5]:
        top.append({
            "amount": transaction["Сумма операции"],
            "category": transaction["Категория"],
            "date": transaction["Дата операции"][:10],
            "description": transaction["Описание"],
        })

    return top


def currency_rates(currency_list: list) -> list:
    """Возвращает стоимость валют из заданного списка через API"""
    return get_currency_rates(currency_list)


def main_page(date: datetime) -> str:
    """Принимает на вход текущую дату и возвращает JSON с расходами и кэшбэком по каждой карте, топ-5 транзакций
    по сумме платежа, курс валют и стоимость акций указанных в файле user_settings.json"""
    if 4 <= date.hour < 10:
        greeting = "Доброе утро"
    elif 10 <= date.hour < 17:
        greeting = "Добрый день"
    elif 17 <= date.hour < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    month_start = datetime(date.year, date.month, 1)

    data = excel_reader(f"{DATA_DIR}\\operations.xlsx")
    data_records = data.to_dict("records")

    filtered_data = []
    for line in data_records:
        if datetime.strptime(line.get("Дата операции"), "%d.%m.%Y %H:%M:%S") >= month_start:
            filtered_data.append(line)

    with open(f"{CONF_DIR}\\user_settings.json") as json_file:
        user_settings = json.load(json_file)

    filtered_dataframe = pd.DataFrame(filtered_data)

    result = {
        "greeting": greeting,
        "cards": cards_collector(filtered_dataframe),
        "top_transactions": top_transactions(filtered_dataframe),
        "currency_rates": get_currency_rates(user_settings.get("user_currencies")),
        "stock_prices": get_stock_prices(user_settings.get("user_stocks")),
    }

    return json.dumps(result)
