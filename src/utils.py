import os
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from src.logger import get_logger

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"
ENV_DIR = ROOT_DIR / ".env"

logger = get_logger("logger", f"{LOGS_DIR}\\{os.path.basename(os.path.abspath(__file__))}.log")

# Загружаем API-токен из .env
load_dotenv(ENV_DIR)

CURRENCY_RATE_API_KEY = os.getenv("CURRENCY_RATE_API_KEY")
STOCK_PRICES_API_KEY = os.getenv("STOCK_PRICES_API_KEY")


def excel_reader(filepath: str = "") -> Any:
    """Принимает на вход путь к файлу формата .xlsx и возвращает список словарей с данными из файла"""
    try:
        data = pd.read_excel(filepath)
    except Exception:
        logger.warning(Exception)
        raise Exception
    logger.info("Функция excel_reader выполнена успешно")
    return data


def get_currency_rates(currency_list: list) -> list:
    """Обращение к внешнему API. Возвращает курсы валют из списка"""

    currencies = ""
    for currency in currency_list:
        currencies += currency + "RUB" + ","
    currencies = currencies[:-1]
    url = f"https://currate.ru/api/?get=rates&pairs={currencies}&key={CURRENCY_RATE_API_KEY}"
    response = requests.request("GET", url)
    status_code = response.status_code

    if status_code == 400:
        logger.warning("Bad Request")
        print("Bad Request")
    if status_code == 401:
        logger.warning("Unauthorized")
        print("Unauthorized")
    if status_code == 404:
        logger.warning("Not Found")
        print("Not Found")
    if status_code == 429:
        logger.warning("Too many requests")
        print("Too many requests")
    if status_code == 500:
        logger.warning("Server Error")
        print("Server Error")

    result = response.json().get("data")
    currency_rates = []
    for currency, rate in result.items():
        currency_rates.append({"currency": currency[:-3], "rate": float(rate)})
    logger.info("Функция get_currency_rates выполнена успешно")
    return currency_rates


def get_stock_prices(stock_list: list) -> list:
    """Обращение к внешнему API. Возвращает курсы акций из списка"""
    stocks = ",".join(stock_list)
    url = f"https://api.marketstack.com/v1/eod?access_key={STOCK_PRICES_API_KEY}"
    querystring = {"symbols": stocks}
    response = requests.get(url, params=querystring)
    status_code = response.status_code
    if status_code == 400:
        logger.warning("Bad Request")
        print("Bad Request")
    if status_code == 401:
        logger.warning("Unauthorized")
        print("Unauthorized")
    if status_code == 403:
        logger.warning("Forbidden")
        print("Forbidden")
    if status_code == 404:
        logger.warning("Not Found")
        print("Not Found")
    if status_code == 429:
        logger.warning("Too many requests")
        print("Too many requests")
    if status_code == 500:
        logger.warning("Server Error")
        print("Server Error")

    result = response.json()
    # yesterday_date = str(datetime.now() - timedelta(days=1)).split(" ")[0]     # Под изначальный сценарий (вчера)
    stock_prices = []
    for stock in result.get("data"):
        # if yesterday_date in stock.get("date"):    # Изначально функция должна была смотреть только на вчерашнюю дату
        stock_prices.append({"price": stock.get("close"), "stock": stock.get("symbol")})

    logger.info("Функция get_stock_prices выполнена успешно")
    return stock_prices
