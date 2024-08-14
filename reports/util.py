from bd.model import Session
from arrow import utcnow, get
from typing import List, Tuple
from pprint import pprint


# Принимает словарь с данными о продукте


def period_to_date(period: str) -> utcnow:
    """
    :param period: day, week,  fortnight, month, two months,
    :return: utcnow - period
    """
    if period == "day":
        return utcnow().to("local").replace(hour=3, minute=00).isoformat()
    if period == "week":
        return (
            utcnow().to("local").shift(days=-7).replace(hour=3, minute=00).isoformat()
        )
    if period == "fortnight":
        return (
            utcnow().to("local").shift(days=-14).replace(hour=3, minute=00).isoformat()
        )
    if period == "month":
        return (
            utcnow().to("local").shift(months=-1).replace(hour=3, minute=00).isoformat()
        )
    if period == "two months":
        return (
            utcnow().to("local").shift(months=-2).replace(hour=3, minute=00).isoformat()
        )
    if period == "6 months":
        return (
            utcnow().to("local").shift(months=-6).replace(hour=3, minute=00).isoformat()
        )
    if period == "12 months":
        return (
            utcnow()
            .to("local")
            .shift(months=-12)
            .replace(hour=3, minute=00)
            .isoformat()
        )
    if period == "24 months":
        return (
            utcnow()
            .to("local")
            .shift(months=-24)
            .replace(hour=3, minute=00)
            .isoformat()
        )
    if period == "48 months":
        return (
            utcnow()
            .to("local")
            .shift(months=-48)
            .replace(hour=3, minute=00)
            .isoformat()
        )
    raise Exception("Period is not supported")


def period_to_date_2(period: str) -> utcnow:
    """
    :param period: day, week,  fortnight, month, two months,
    :return: utcnow + period
    """
    if period == "day":
        return utcnow().replace(hour=3, minute=00).isoformat()
    if period == "week":
        return utcnow().shift(days=7).replace(hour=3, minute=00).isoformat()
    if period == "fortnight":
        return utcnow().shift(days=14).replace(hour=3, minute=00).isoformat()
    if period == "month":
        return utcnow().shift(months=1).replace(hour=3, minute=00).isoformat()
    if period == "two months":
        return utcnow().shift(months=2).replace(hour=3, minute=00).isoformat()
    if period == "6 months":
        return utcnow().shift(months=6).replace(hour=3, minute=00).isoformat()
    if period == "12 months":
        return utcnow().shift(months=12).replace(hour=3, minute=00).isoformat()
    if period == "24 months":
        return utcnow().shift(months=24).replace(hour=3, minute=00).isoformat()
    if period == "48 months":
        return utcnow().shift(months=48).replace(hour=3, minute=00).isoformat()
    raise Exception("Period is not supported")


def get_intervals(
    min_date: str, max_date: str, unit: str, measure: float
) -> List[Tuple[str, str]]:
    """
    :param min_date: дата начала пириода
    :param max_date: дата окончания пириода
    :param unit: days, weeks,  fortnights, months
    :param measure: int шаг
    :return: List[Tuple[min_date, max_date]]
    """
    output = []
    while min_date < max_date:
        # записывет в перменную temp минимальную дату плюс (unit: measure)
        temp = get(min_date).shift(**{unit: measure}).isoformat()
        # записывает в output пару дат min_date и  меньшую дату min_date max_date или temp
        output.append((min_date, min(temp, max_date)))
        # меняет значение min_date на temp
        min_date = temp
    return output


def get_period(session: Session):
    """
    :param session:
    :return: {'since': str, 'until': str}
    """
    period_in = ["day", "week", "fortnight", "month"]
    if session.params["inputs"]["0"]["period"] not in period_in:
        return {
            "since": get(session.params["inputs"]["0"]["openDate"])
            .replace(day=1)
            .isoformat(),
            "until": get(session.params["inputs"]["0"]["openDate"])
            .ceil("month")
            .isoformat(),
        }
    if session.params["inputs"]["0"]["period"] == "day":
        return {
            "since": period_to_date(session.params["inputs"]["0"]["period"]),
            "until": utcnow().isoformat(),
        }

    else:
        return {
            "since": get(session.params["inputs"]["0"]["openDate"])
            .replace(hour=3, minute=00)
            .isoformat(),
            "until": get(session.params["inputs"]["0"]["closeDate"])
            .replace(hour=23, minute=00)
            .isoformat(),
        }


def get_period_day(session: Session):
    """
    :param session:
    :return: {'since': str, 'until': str}
    """
    if session.params["inputs"]["0"]["period"] == "day":
        return {
            "since": period_to_date(session.params["inputs"]["0"]["period"]),
            "until": get(period_to_date(session.params["inputs"]["0"]["period"]))
            .replace(hour=23, minute=00)
            .isoformat(),
        }

    else:
        return {
            "since": get(session.params["inputs"]["0"]["openDate"])
            .replace(hour=0, minute=1)
            .isoformat(),
            "until": get(session.params["inputs"]["0"]["openDate"])
            .replace(hour=23, minute=59)
            .isoformat(),
        }


def format_reminder(input_dict: dict) -> dict:
    """
    Форматирует данный словарь, заменяя ключи на заданные метки.

    Аргументы:
        input_dict (dict): Словарь, содержащий данные напоминания. Ожидаются следующие ключи:
            - 'text' (str): Текст напоминания.
            - 'user_id' (str): ID пользователя.
            - 'status_type' (str): Статус напоминания (например, "active").
            - 'date' (str): Дата и время создания напоминания в формате ISO 8601 (например, "2024-07-27T14:00:00+00:00").
            - 'link' (str): Ссылка, связанная с напоминанием.
            - 'month' (str): Месяц напоминания (например, "Июль").
            - 'day_of_month' (str): День месяца напоминания (например, "27").
            - 'time' (str): Время напоминания в формате "HH:MM" (например, "14:00").
            - 'reminder_name' (str): Название напоминания.

    Возвращает:
        dict: Новый словарь, где ключи заменены на специальные метки, а значения взяты из входного словаря.
        Ключи нового словаря соответствуют меткам из словаря `data`:
            - "📋 Текст напоминания:" для 'text'
            - "👤 ID пользователя:" для 'user_id'
            - "📅 Статус напом." для 'status_type'
            - "🕒 Дата создания:" для 'date'
            - "📅 Месяц напом.:" для 'month'
            - "📅 День недели напом.:" для 'month'
            - "📅 День месяца напом.:" для 'day_of_month'
            - "⏰ Время напом.:" для 'time'
            - "📌 Название напом.:" для 'reminder_name'
    """
    data = {
        "text": "📋 Текст напоминания:",
        "user_id": "👤 ID пользователя:",
        "status_type": "📅 Статус напом.",
        "date": "🕒 Дата создания:",
        "month": "📅 Месяц напом.:",
        "week_day": "📅 День недели",
        "day_of_month": "📅 День месяца напом.:",
        "time": "⏰ Время напом.:",
        "chat_name": "💬 Название чата:",
        "reminder_name": "📌 Название напом.:",
        "TZ": "🌍 Часовой пояс:",
    }

    formatted_dict = {}
    for k, v in input_dict.items():
        if k in data:
            if k == "date":
                formatted_dict[data[k]] = v[:16]
            else:
                formatted_dict[data[k]] = v

    return formatted_dict
