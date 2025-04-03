from datetime import datetime
import re

def format_date(date_str: str):
    """Приведение даты к единому формату."""
    # Убираем лишние пробелы и символы, чтобы иметь возможность парсить дату
    date_str = date_str.strip()
    
    # Пробуем разные шаблоны для дат
    try:
        # Форматируем в "День Месяц Год г."
        return datetime.strptime(date_str, "%d %B %Y").strftime("%d %B %Y г.")
    except ValueError:
        pass
    
    try:
        # Форматируем для: "день.месяц.год"
        return datetime.strptime(date_str, "%d.%m.%Y").strftime("%d %B %Y г.")
    except ValueError:
        pass

    try:
        # Форматируем для: "день-месяц-год"
        return datetime.strptime(date_str, "%d-%m-%Y").strftime("%d %B %Y г.")
    except ValueError:
        pass

    # Если не получилось, возвращаем None
    return None

def parse_date_range(date_str: str):
    """Функция для преобразования разных форматов дат в один формат"""
    # Проверка на диапазон "с ... по ..."
    if "по" in date_str:
        parts = date_str.split("по")
        start_date = format_date(parts[0].strip())
        end_date = format_date(parts[1].strip())
        if start_date and end_date:
            return f"{start_date} - {end_date}"

    # Проверка на диапазоны типа "день - день"
    elif "-" in date_str:
        parts = date_str.split("-")
        start_date = format_date(parts[0].strip())
        end_date = format_date(parts[1].strip())
        if start_date and end_date:
            return f"{start_date} - {end_date}"

    # Для одиночных дат
    else:
        single_date = format_date(date_str)
        return single_date if single_date else None


# Примеры:
dates = [
    "23 - 25 сентября 2022 г.",
    "с 17 сентября по 19 ноября 2021",
    "23 - 25 августа 2023 г.",
    "29-01-2022",
    "20 октября, с 10:00 до 10:30 по Самарскому времени",
    "30 октября, с 10:00 до 18:30 по Московскому времени",
    "22.10 - 24.10.2021"
]

for date in dates:
    print(parse_date_range(date))
