from bd.model import Session, Chat, Post
from .util import format_reminder

from arrow import utcnow, get
import sys

import logging

logger = logging.getLogger(__name__)


name = "✨ Reminder ➡️".upper()
desc = ""
mime = "text"


class ReminderMenuInput:
    """
    Меню напоминаний
    """

    name = "Выберете".upper()
    desc = "Выберете".upper()
    type = "SELECT"

    def get_options(self, session: Session):
        output = [
            {"id": "add_reminder", "name": "➕ ДОБАВИТЬ НАПОМИНАНИЕ ➡️"},
            {"id": "edit_reminder", "name": "✏️ 👁️ ПРОСМОТРЕТЬ/✏️ ИЗМЕНИТЬ НАПОМИНАНИЕ ➡️"},
            # {"id": "view_reminders", "name": "👁️ ПРОСМОТРЕТЬ НАПОМИНАНИЯ ➡️"},
        ]

        return output


class ReminderActionMenuInput:
    """
    Меню напоминаний
    """

    name = "Выберете".upper()
    desc = "Выберете".upper()
    type = "SELECT"

    def get_options(self, session: Session):
        output = [
            {"id": "view_reminder", "name": "👁️ ПРОСМОТРЕТЬ ➡️"},
            {"id": "change_reminder", "name": "✏️ ИЗМЕНИТЬ НАПОМИНАНИЕ ➡️"},
            {"id": "delete_reminders", "name": "❌ УДАЛИТЬ НАПОМИНАНИЯ ➡️"},
        ]

        return output


class ChangeAReminderInput:
    """
    Меню напоминаний
    """

    name = "Выберете".upper()
    desc = "Выберете".upper()
    type = "SELECT"

    def get_options(self, session: Session):
        output = [
            {"id": "change_period", "name": "📅 ИЗМЕНИТЬ ПЕРИОД ➡️"},
            {"id": "change_reminder", "name": "✏️ ИЗМЕНИТЬ ТЕКСТ НАПОМИНАНИЯ ➡️"},
        ]

        return output


class GetChatInput:
    """
    Класс для получения  и добавления списка чатов
    """

    desc = "Выберите чат"
    type = "SELECT"

    def get_options(self, session: Session):
        output = []

        data_chats = Chat.objects(user_id=session.user_id).first()

        if data_chats:

            for item in Chat.objects(user_id=session.user_id, status_type="active"):

                name = item["chat_title"]
                output.append({"id": item["chat_id"], "name": f"{name} ➡️"})

        return output


class NameReminderInput:
    desc = "Напишите название напоминания ✍️".upper()
    type = "MESSAGE"


class TextInput:
    desc = "Напишите текст напоминания ✍️".upper()
    type = "MESSAGE"


class PeriodInput:
    name = "Выберите период 📅".upper()
    desc = "Выберите месяц 📅".upper()
    type = "SELECT"

    def get_options(self, session: Session):
        return [
            {"id": "one_time", "name": "🕒 ОДИН РАЗ ➡️"},
            {"id": "daily", "name": "📅 ЕЖЕДНЕВНО ➡️"},
            {"id": "weekly", "name": "📅 ЕЖЕНЕДЕЛЬНО ➡️"},
            {"id": "monthly", "name": "📅 ЕЖЕМЕСЯЧНО ➡️"},
            {"id": "yearly", "name": "📅 ЕЖЕГОДНО ➡️"},
        ]


class MonthInput:
    """
    Запрос месяца
    """

    name = "Выберите месяц 📅".upper()
    desc = "Выберите месяц 📅".upper()
    type = "SELECT"

    def get_options(self, session: Session):
        """
        Получение опций для выбора месяца.
        """
        return [
            {"id": "jan", "name": "ЯНВАРЬ ➡️"},
            {"id": "feb", "name": "ФЕВРАЛЬ ➡️"},
            {"id": "mar", "name": "МАРТ ➡️"},
            {"id": "apr", "name": "АПРЕЛЬ ➡️"},
            {"id": "may", "name": "МАЙ ➡️"},
            {"id": "jun", "name": "ИЮНЬ ➡️"},
            {"id": "jul", "name": "ИЮЛЬ ➡️"},
            {"id": "aug", "name": "АВГУСТ ➡️"},
            {"id": "sep", "name": "СЕНТЯБРЬ ➡️"},
            {"id": "oct", "name": "ОКТЯБРЬ ➡️"},
            {"id": "nov", "name": "НОЯБРЬ ➡️"},
            {"id": "dec", "name": "ДЕКАБРЬ ➡️"},
        ]


class DayOfMonthInput:
    """
    Запрос числа месяца
    """

    name = "Введите число месяца 📅".upper()
    desc = "Напишите число месяца в формате ДД(00) ✍️".upper()
    type = "MESSAGE"


class WeekDayInput:
    """
    Запрос дня недели
    """

    name = "Выберите день недели 📅".upper()
    desc = "Выберите день недели 📅".upper()
    type = "SELECT"

    def get_options(self, session: Session):
        return [
            {"id": "mon", "name": "ПОНЕДЕЛЬНИК ➡️"},
            {"id": "tue", "name": "ВТОРНИК ➡️"},
            {"id": "wed", "name": "СРЕДА ➡️"},
            {"id": "thu", "name": "ЧЕТВЕРГ ➡️"},
            {"id": "fri", "name": "ПЯТНИЦА ➡️"},
            {"id": "sat", "name": "СУББОТА ➡️"},
            {"id": "sun", "name": "ВОСКРЕСЕНЬЕ ➡️"},
        ]


class TimeZoneInput:
    """
    Запрос часового пояса
    """

    name = "ВЫБЕРИТЕ ЧАСОВОЙ ПОЯС 🕒".upper()
    desc = "ВЫБЕРИТЕ ЧАСОВОЙ ПОЯС 🕒".upper()
    type = "SELECT"

    def get_options(self, session: Session):
        return [
            {"id": "-12", "name": "UTC-12 ➡️"},
            {"id": "-11", "name": "UTC-11 ➡️"},
            {"id": "-10", "name": "UTC-10 ➡️"},
            {"id": "-09", "name": "UTC-09 ➡️"},
            {"id": "-08", "name": "UTC-08 ➡️"},
            {"id": "-07", "name": "UTC-07 ➡️"},
            {"id": "-06", "name": "UTC-06 ➡️"},
            {"id": "-05", "name": "UTC-05 ➡️"},
            {"id": "-04", "name": "UTC-04 ➡️"},
            {"id": "-03", "name": "UTC-03 ➡️"},
            {"id": "-02", "name": "UTC-02 ➡️"},
            {"id": "-01", "name": "UTC-01 ➡️"},
            {"id": "+00", "name": "UTC+00 ➡️"},
            {"id": "+01", "name": "UTC+01 ➡️"},
            {"id": "+02", "name": "UTC+02 ➡️"},
            {"id": "+03", "name": "UTC+03 ➡️"},
            {"id": "+04", "name": "UTC+04 ➡️"},
            {"id": "+05", "name": "UTC+05 ➡️"},
            {"id": "+06", "name": "UTC+06 ➡️"},
            {"id": "+07", "name": "UTC+07 ➡️"},
            {"id": "+08", "name": "UTC+08 ➡️"},
            {"id": "+09", "name": "UTC+09 ➡️"},
            {"id": "+10", "name": "UTC+10 ➡️"},
            {"id": "+11", "name": "UTC+11 ➡️"},
            {"id": "+12", "name": "UTC+12 ➡️"},
        ]


class TimeInput:
    """
    Запрос времени
    """

    name = "Введите время 🕒".upper()
    desc = "Напишите время в формате HH:MM(00:00) ✍️".upper()
    type = "MESSAGE"


class GetPostInput:
    """
    Класс для получения списка постов
    """

    desc = "Выберите чат"
    type = "SELECT"

    def get_options(self, session: Session):
        output = []

        data_chats = Post.objects(user_id=session.user_id).first()

        if data_chats:
            for item in Post.objects(user_id=session.user_id, status_type="active"):
                reminder_name = item["reminder_name"]
                output.append({"id": item["date"], "name": f"{reminder_name} ➡️"})
        return output


def get_period_inputs(period):
    """
    Возвращает необходимые вводы на основе выбранного периода.
    """
    if period == "one_time":
        return {
            "month": MonthInput,
            "day_of_month": DayOfMonthInput,
            "time": TimeInput,
        }

    elif period == "daily":
        return {"time": TimeInput}

    elif period == "weekly":
        return {"week_day": WeekDayInput, "time": TimeInput}

    elif period == "monthly":
        return {"day_of_month": DayOfMonthInput, "time": TimeInput}

    elif period == "yearly":
        return {
            "month": MonthInput,
            "day_of_month": DayOfMonthInput,
            "time": TimeInput,
        }

    return {}


def get_inputs(session: Session):
    """
    Функция для определения необходимых вводов на основе выбранного типа напоминания и периода.
    """
    try:
        # Получение входных данных из сессии
        inputs = session.params.get("inputs", {}).get("0", {})

        # Если нет входных данных, возвращаем главное меню напоминаний
        if not inputs:
            return {
                "report": ReminderMenuInput,
            }

        # Получение типа напоминания
        report_type = inputs.get("report", None)

        # Обработка добавления напоминания
        if report_type == "add_reminder":
            # Проверка наличия chat_id
            chat_id = inputs.get("chat_id")
            tz = inputs.get("TZ")

            if not chat_id:
                # if Chat.objects(chat_id__in=chat_id).
                return {"chat_id": GetChatInput}
            # print(type(chat_id))
            # print(vars(Chat.objects(chat_id=int(chat_id)).first()))

            if Chat.objects(chat_id=int(chat_id)).first().TZ == None:
                if not tz:
                    return {"TZ": TimeZoneInput}

            # Проверка наличия имени напоминания
            reminder_name = inputs.get("reminder_name")
            if not reminder_name:
                return {"reminder_name": NameReminderInput}
            # Проверка наличия текста
            text = inputs.get("text")
            if not text:
                return {"text": TextInput}

            # Проверка наличия периода
            period = inputs.get("period")
            if not period:
                return {"period": PeriodInput}

            # Обработка в зависимости от выбранного периода
            return get_period_inputs(period)

        # Проверка на случай, если выбран "редактировать напоминание" или "просмотреть напоминания"
        if report_type == "edit_reminder":
            # Проверка наличия ссылки
            reminder_date = inputs.get("reminder_date")
            if not reminder_date:
                return {"reminder_date": GetPostInput}

            # Проверка наличия действия для напоминания
            action = inputs.get("action")
            if not action:
                return {"action": ReminderActionMenuInput}

            if action == "change_reminder":
                change = inputs.get("change")

                if not change:
                    return {"change": ChangeAReminderInput}

                # Обработка изменения периода напоминания
                if change == "change_period":
                    period = inputs.get("period")
                    if not period:
                        return {"period": PeriodInput}

                    # Обработка в зависимости от выбранного периода
                    return get_period_inputs(period)

                if change == "change_reminder":
                    return {"text": TextInput}

            if action in ["delete_reminders", "view_reminder"]:
                return {}
        # Если ни одно из условий не выполнено, возвращаем пустой словарь
        return {}

    except Exception as e:
        logger.error(f"Ошибка: {e} на строке {sys.exc_info()[-1].tb_lineno}")


def generate(session: Session):
    try:
        # Получаем входные данные из сессии
        inputs = session.params.get("inputs", {}).get("0", {})
        logger.info(inputs)

        # Определяем тип отчета
        report_type = inputs.get("report")

        time_zone = inputs.get("TZ")

        if time_zone:
            # Проверка наличия chat_id
            chat_id = inputs.get("chat_id")
            params = {"TZ": time_zone}
            Chat.objects(chat_id=int(chat_id)).update(**params, upsert=True)

        if report_type == "add_reminder":
            # Получаем параметры для напоминания
            chat_id = inputs.get("chat_id")
            month = inputs.get("month", None)
            day_of_month = inputs.get("day_of_month", None)
            time = inputs.get("time", None)
            reminder_name = inputs.get("reminder_name", None)

            chat = Chat.objects(chat_id=int(chat_id)).first()

            print(vars(chat))
            post = {
                "text": inputs.get("text"),
                "user_id": session.user_id,
                "status_type": "active",
                "date": utcnow().to("local").isoformat(),
                "chat_id": chat_id,
                "month": month,
                "day_of_month": day_of_month,
                "time": time,
                "chat_name": chat.chat_title,
                "reminder_name": reminder_name,
                "TZ": chat.TZ,
            }

            report_data = format_reminder(post)

            logger.info(post)
            # Обновляем или создаем запись в коллекции Post
            Post.objects(date=post["date"]).update(**post, upsert=True)
            return [report_data]

        # Если тип отчета "edit_reminder", редактируем существующее напоминание
        if report_type == "edit_reminder":

            reminder_date = inputs.get("reminder_date", None)
            print(reminder_date)
            change = inputs.get("change")
            action = inputs.get("action")

            if action == "delete_reminders":
                post = {
                    "status_type": "delete",
                    "date": utcnow().to("local").isoformat(),
                }
                logger.info(post)
                Post.objects(date=reminder_date).update(**post, upsert=True)

                post = Post.objects(date=reminder_date).first()

                report_data = format_reminder(post)

                return [report_data]
            if action == "view_reminder":
                post = Post.objects(date=reminder_date).first()
                chat = Chat.objects(chat_id=int(post.chat_id)).first()

                report_data = {
                    "📋 Текст напоминания:": post["text"],
                    "👤 ID пользователя:": post.user_id,
                    "📅 Статус напом.:": post.status_type,
                    "🕒 Дата создания:": post["date"][:10],
                    "💬 chat_name:": post.chat_name,
                    "📅 Месяц напом.:": post.month,
                    "📅 День месяца напом.:": post.day_of_month,
                    "⏰ Время напом.:": post.time,
                    "📌 Название напом.:": post["reminder_name"],
                    "🌍 Часовой пояс:": chat.TZ,
                }
                return [report_data]
            if change:
                post = Post.objects(date=reminder_date).first()
                chat = Chat.objects(chat_id=int(post.chat_id)).first()

                print(post["reminder_name"])
                if change == "change_period":
                    print("change_period")
                    month = inputs.get("month", None)
                    day_of_month = inputs.get("day_of_month", None)
                    time = inputs.get("time", None)

                    post_ = {
                        "date": utcnow().to("local").isoformat(),
                        "month": month,
                        "day_of_month": day_of_month,
                        "time": time,
                        "reminder_name": post["reminder_name"],
                    }

                    report_data = {
                        "📋 Текст напоминания:": post["text"],
                        "👤 ID пользователя:": post.user_id,
                        "📅 Статус:": post.status_type,
                        "🕒 Дата:": post_["date"][:16],
                        "💬 chat_name:": post.chat_name,
                        "📅 Месяц:": month,
                        "📅 День месяца:": day_of_month,
                        "⏰ Время:": time,
                        "📌 Название напоминания:": post["reminder_name"],
                        "🌍 Часовой пояс:": chat.TZ,
                    }

                if change == "change_reminder":
                    text = inputs.get("text", None)

                    post_ = {
                        "text": text,
                        "reminder_name": post["reminder_name"],
                    }

                    report_data = {
                        "📋 Текст напоминания:": text,
                        "👤 ID пользователя:": post.user_id,
                        "📅 Статус:": post.status_type,
                        "🕒 Дата:": post["date"][:16],
                        "💬 chat_name:": post.chat_name,
                        "📅 Месяц:": post.month,
                        "📅 День месяца:": post.day_of_month,
                        "⏰ Время:": post.time,
                        "📌 Название напоминания:": post["reminder_name"],
                        "🌍 Часовой пояс:": chat.TZ,
                    }
                logger.info(post_)
                logger.info(report_data)
                Post.objects(date=reminder_date).update(**post_, upsert=True)

                return [report_data]

    except Exception as e:
        # Логируем ошибку, если что-то пошло не так
        # logger.error(f"Произошла ошибка: {e}")
        logger.error(f"Ошибка: {e} на строке {sys.exc_info()[-1].tb_lineno}")
