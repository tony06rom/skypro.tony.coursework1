import datetime
import json
import os
from pathlib import Path
import pandas as pd

from src.logger import get_logger

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"

logger = get_logger("logger", f"{LOGS_DIR}\\{os.path.basename(os.path.abspath(__file__))}.log")


def cashback_category(data: pd.DataFrame, year: int, month: int) -> str:
    """Возвращает JSON и показывает сколько можно заработать кэшбэка по каждой категории в указанном месяце года"""
    categories: dict[str, int] = {}
    print(type(categories))
    # data = data.to_dict("records")
    data_records = data.to_dict("records")
    print(type(data))
    for operation in data_records:
        date = datetime.datetime.strptime(operation["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if date.month == month and date.year == year:
            category = operation.get("Категория")
            cashback = operation.get("Кэшбэк")
            if category is not None and cashback is not None and cashback > 0:
                if category not in categories:
                    categories[category] = int(cashback)
                else:
                    categories[category] += int(cashback)
            # if categories.get(operation.get("Категория")) is None:
            #     if operation.get("Кэшбэк") is not None and operation.get("Кэшбэк") > 0:
            #         categories[operation.get("Категория")] = int(operation.get("Кэшбэк"))
            # else:
            #     if operation.get("Кэшбэк") is not None and operation.get("Кэшбэк") > 0:
            #         categories[operation.get("Категория")] += int(operation.get("Кэшбэк"))

    categories_sorted = sorted(categories.items(), key=lambda item: item[1], reverse=True)
    print(categories)
    logger.debug("Список отсортирован по убыванию кэшбэка")
    result: dict[str | str, int | str] = {}
    print(type(categories))
    for category in categories_sorted:
        result[category[0]] = category[1]
    # result = {key: value for key, value in categories_sorted}

    logger.info("Функция выполнена успешно")
    return json.dumps(result)
