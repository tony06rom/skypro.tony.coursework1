import datetime
import os
from collections.abc import Callable
from pathlib import Path
from typing import Optional

import pandas as pd

from src.logger import get_logger

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"

logger = get_logger("logger", f"{LOGS_DIR}\\{os.path.basename(os.path.abspath(__file__))}.log")


def report(filename: str = "report.csv"):
    """Декоратор записывает в файл результат работы функции"""

    def decorator(func: Callable) -> object:
        def wrapper(*args: str, **kwargs: int) -> object:
            result = func(*args, **kwargs)
            logger.info("Основная функция выполнена успешно")
            with open(f"{DATA_DIR}\\{filename}", "w", newline="") as file:
                result.to_csv(file, sep=" ", index=False, encoding="utf-8")
                logger.info(f"Отчет сохранен в файле {DATA_DIR}\\{filename}")
                print(f"Отчет сохранен в файле {DATA_DIR}\\{filename}")
            return result

        return wrapper

    return decorator


@report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает список трат по заданной категории в заданном периоде"""
    logger.debug(transactions)
    if date is None:
        date = datetime.date.today()
    else:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")
    second_date = date - datetime.timedelta(days=90)
    transactions = transactions.loc[:, ["Категория", "Дата операции", "Сумма операции"]]
    logger.info("Выполняется фильтрация значений по дате и категории")
    try:
        result = transactions.loc[
            (transactions["Категория"] == category)
            & (pd.to_datetime(transactions["Дата операции"], dayfirst=True) >= second_date)
            & (pd.to_datetime(transactions["Дата операции"], dayfirst=True) <= date)
            & (transactions["Сумма операции"] < 0)
        ]
    except Exception:
        logger.warning(Exception)
        raise Exception
    logger.debug(result)
    logger.info("Фильтрация выполнена успешно")
    return result
