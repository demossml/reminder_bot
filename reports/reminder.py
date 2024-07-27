from bd.model import Session, Chat, Post

from arrow import utcnow, get
import sys

import logging

logger = logging.getLogger(__name__)


name = "✨ Post ➡️".upper()
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
    


class LinkInput:
    desc = "Напишите адрес формате @chat_name ✍️".upper()
    type = "MESSAGE"


class GetLinkInput:
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
                for link in item["link"]:
                    output.append({"id": link, "name": f"{link} ➡️"})

        output.append(
            {"id": "add_chat", "name": "➕ ДОБАВИТЬ ЧАТ ➡️"},
        )
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
                output.append({"id": item["date"], "name": f"{item["reminder_name"]} ➡️"})
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
            # Проверка наличия ссылки
            link = inputs.get("link")
            if not link:
                return {"link": GetLinkInput}

            # Если выбран пункт добавления чата
            if link == "add_chat":
                # Проверка наличия имени напоминания
                reminder_name = inputs.get("reminder_name")
                if not reminder_name:
                    return {"reminder_name": NameReminderInput}

                # Проверка наличия имени ссылки
                link_name = inputs.get("link_name")
                if not link_name:
                    return {"link_name": LinkInput}

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

            # Обработка для других случаев
            else:
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
            reminder_name = inputs.get("reminder_name")
            if not reminder_name:
                return {"reminder_name": GetPostInput} 
            
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
   

        if report_type == "add_reminder":
            # Получаем параметры для напоминания
            link_name = inputs.get("link_name", None)
            link = inputs.get("link")
            month = inputs.get("month", None)
            day_of_month = inputs.get("day_of_month", None)
            time = inputs.get("time", None)
            reminder_name = inputs.get("reminder_name", None)

            # Проверяем, нужно ли добавить ссылку в чат
            if link == "add_chat":
                # Ищем чат пользователя по user_id
                chat = Chat.objects(user_id=session.user_id).first()

                if chat:

                    # Если чат существует, добавляем новую ссылку к существующим
                    chat_link = chat.link if chat.link else []
                    if link_name not in chat_link:
                        chat_link.append(link_name)
                else:
                    # Если чат не существует, создаем новый список ссылок
                    chat_link = [link_name]

                # Подготавливаем параметры для обновления или создания записи
                params = {
                    "user_id": session.user_id,
                    "status_type": "active",
                    "date": utcnow().to("local").isoformat(),
                    "link": chat_link,
                }

                # Обновляем или создаем запись в коллекции Chat
                Chat.objects(user_id=session.user_id).update(**params, upsert=True)
                
                # Подготавливаем данные для создания нового напоминания
                post = {
                    "text": inputs.get("text"),
                    "user_id": session.user_id,
                    "status_type": "active",
                    "date": utcnow().to("local").isoformat(),
                    "link": link_name,
                    "month": month,
                    "day_of_month": day_of_month,
                    "time": time,
                    "reminder_name": reminder_name,
                }

            else:
                # Подготавливаем данные для создания нового напоминания
                post = {
                    "text": inputs.get("text"),
                    "user_id": session.user_id,
                    "status_type": "active",
                    "date": utcnow().to("local").isoformat(),
                    "link": link,
                    "month": month,
                    "day_of_month": day_of_month,
                    "time": time,
                    "reminder_name": reminder_name,
                }
            logger.info(post)
            # Обновляем или создаем запись в коллекции Post
            Post.objects(date=post["date"]).update(**post, upsert=True)
            return [post]
        
        # Если тип отчета "edit_reminder", редактируем существующее напоминание
        if report_type == "edit_reminder":
            
            reminder_name = inputs.get("reminder_name", None)
            print(reminder_name)
            change = inputs.get("change")
            action = inputs.get("action")
            
            if action == "delete_reminders":
                post = {
                    "status_type": "delete",
                    "date": utcnow().to("local").isoformat(),
                 
                }
                logger.info(post)
                Post.objects(date=reminder_name).update(**post, upsert=True)
                
                return  [
                    {
    
                        "Status type:":  "delete",
                        "Reminder name:": reminder_name,
                            
                    }
                ]
            
            if action == "view_reminder":
                post = Post.objects(date=reminder_name).first()
                
                return  [
                    {
                        "Text:": post["text"],
                        "User_id:": post.user_id,
                        "Status type:": post.status_type,
                        "Date:": post.date[:16],
                        "Link:": post.link,
                        "Month:": post.month,
                        "Day:": post.day_of_month,
                        "Time:": post.time,
                        "Reminder name:": post.reminder_name,
                            
                    }
                ]
                
            
            if change:
                post = Post.objects(date=reminder_name).first()
                if change == "change_period":
                    month = inputs.get("month", None)
                    day_of_month = inputs.get("day_of_month", None)
                    time = inputs.get("time", None)
        
                    post = {
                    "date": utcnow().to("local").isoformat(),
                    "month": month,
                    "day_of_month": day_of_month,
                    "time": time,
                    "reminder_name": post.reminder_name,
                    }
                
                if change == "change_reminder":
                    text = inputs.get("text", None)
                    link_name = inputs.get("link_name", None)
                    link = inputs.get("link")
                    month = inputs.get("month", None)
                    day_of_month = inputs.get("day_of_month", None)
                    time = inputs.get("time", None)
                    reminder_name = inputs.get("reminder_name", None)
                
                    post = {
                        "text": text,
                        "reminder_name": post.reminder_name,

                    }
                    
                logger.info(post)
                Post.objects(date=reminder_name).update(**post, upsert=True)
                return [post]
            
            

    except Exception as e:
        # Логируем ошибку, если что-то пошло не так
        # logger.error(f"Произошла ошибка: {e}")
        logger.error(f"Ошибка: {e} на строке {sys.exc_info()[-1].tb_lineno}")

