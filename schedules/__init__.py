import telebot
import logging
from telebot import types
from telebot.apihelper import ApiTelegramException
from datetime import datetime
import schedule
import time
from bd.model import Chat, Post
import pytz
import threading
import arrow

time_zone_ = {
    "+00": 0,
    "+01": -1,
    "+02": -2,
    "+03": -3,
    "+04": -4,
    "+05": -5,
    "+06": -6,
    "+07": -7,
    "+08": -8,
    "+09": -9,
    "+10": -10,
    "+11": -11,
    "+12": -12,
    "-01": 1,
    "-02": 2,
    "-03": 3,
    "-04": 4,
    "-05": 5,
    "-06": 6,
    "-07": 7,
    "-08": 8,
    "-09": 9,
    "-10": 10,
    "-11": 11,
    "-12": 12,
}

welcome_message = """
👋 Привет! Я - ваш новый помощник по напоминаниям! 🎉

Моя задача - помочь вам и вашей команде никогда не забывать важные задачи и события. Вот что я могу сделать:

📅 Создавать напоминания** о важных делах.
✏️ Изменять существующие напоминания**.
🗑️ Удалять ненужные напоминания**.
📋 Выводить список всех ваших напоминаний**.

Чтобы начать использовать все мои возможности, добавьте меня в свою группу. Это легко сделать:

1. 📌 Нажмите на название группы в верхней части экрана.
2. ➕ Выберите "Добавить участника".
3. 🔍 Введите мой ник: @ReminderPost_bot .
4. 👤 Нажмите на меня и выберите "Добавить".

После добавления в группу, я смогу помогать вам с напоминаниями, отправляя уведомления прямо в чат! 💬

Если вам нужна дополнительная помощь или у вас есть вопросы, просто напишите мне @ds7278, и я предоставлю вам подробную инструкцию.

Спасибо, что выбрали меня! Давайте сделаем вашу работу еще более организованной и эффективной. 🚀
"""


logger = logging.getLogger(__name__)

# Устанавливаем временную зону MSK
msk = pytz.timezone("Europe/Moscow")

# Токен вашего бота
TOKEN = "7482295427:AAHuiiKgdQtqnWLKi8sAWn7AwVcbC2xMafU"
bot = telebot.TeleBot(TOKEN)


btUrlChannel = types.InlineKeyboardButton(
    text="Reminder Manager 📝", url="https://t.me/ReminderManager_bot"
)
channelMenu = types.InlineKeyboardMarkup(row_width=1)
channelMenu.add(btUrlChannel)


# Функция для проверки формата времени
def validate_time_format(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


# Функция для отправки сообщения
def job(chat_id, text):
    try:
        logging.info(f"Отправка сообщения в чат {chat_id} с текстом: {text}")
        bot.send_message(int(chat_id), text)
        logging.info(f"Сообщение успешно отправлено в чат {chat_id}")
    except ApiTelegramException as e:
        logging.error(f"Ошибка при отправке сообщения в чат {chat_id}: {e}")
    except Exception as e:
        logging.error(f"Неизвестная ошибка при отправке сообщения в чат {chat_id}: {e}")


# Функция для планирования сообщений
def schedule_messages():
    # Получаем данные о постах из базы данных
    posts_data = Post.objects(status_type="active")
    logging.info(f"Загружено {len(posts_data)} сообщений из базы данных")

    # Удаляем старые задачи, кроме задачи обновления расписания
    get_jobs = schedule.get_jobs()
    if len(get_jobs) > 0:
        for job_ in get_jobs:
            if "update_schedule" not in job_.tags:
                logging.info(f"Удаление задачи: {job_}")
                schedule.cancel_job(job_)

    # Проходим по каждому посту из базы данных
    for item in posts_data:
        day_of_month = item["day_of_month"]
        month = item["month"]
        text = item["text"]
        time_str = item["time"]
        chat_id = item["chat_id"]
        reminder_name = item["reminder_name"]

        # Получаем часовой пояс для чата
        chat = Chat.objects(chat_id=int(chat_id)).first()
        if chat:
            if chat["TZ"]:
                time_zone = chat["TZ"]
                print(type(time_zone))
                print(type(time_zone_[time_zone]))

                # Получаем текущий год
                now = arrow.now()
                year = now.year

                # Формируем строку даты и времени
                if month and day_of_month:
                    datetime_str = f"{year}-{month:02d}-{day_of_month:02d} {time_str}"
                elif day_of_month:
                    datetime_str = (
                        f"{year}-{now.month:02d}-{day_of_month:02d} {time_str}"
                    )
                else:
                    datetime_str = f"{year}-{now.month:02d}-{now.day:02d} {time_str}"

                logging.info(datetime_str)

                try:
                    # Применяем метод arrow.get(), чтобы создать объект Arrow
                    dt = arrow.get(datetime_str, "YYYY-MM-DD HH:mm").shift(
                        hours=int(time_zone_[time_zone])  # Смещение часового пояса
                    )
                    # Уже сделано смещение, поэтому no need to call .to('UTC') here
                except Exception as e:
                    logging.error(f"Ошибка при обработке даты и времени: {e}")
                    continue

                logging.info(
                    f"Планирование сообщения: time_zone={time_zone}, reminder_name={reminder_name}, чат_id={chat_id}, текст={text}, день={day_of_month}, месяц={month}, время={time_str}"
                )
                logging.info(dt.format("MM-DD HH:mm"))

                # Проверка формата времени
                if not validate_time_format(time_str):
                    logging.error(f"Неверный формат времени: {time_str}")
                    continue

                # Планируем сообщения в зависимости от типа напоминания
                if month and day_of_month:
                    # Ежегодное напоминание в указанный месяц, день и время
                    schedule.every().year.at(dt.format("MM-DD HH:mm")).do(
                        job, chat_id, text
                    ).tag(reminder_name)
                elif day_of_month:
                    # Ежемесячное напоминание в указанный день и время
                    schedule_time = dt.format("HH:mm")

                    def monthly_job():
                        today = arrow.utcnow()
                        if today.day == day_of_month:
                            job(chat_id, text)

                    schedule.every().day.at(schedule_time).do(monthly_job).tag(
                        reminder_name
                    )
                else:
                    # Ежедневное напоминание в указанное время, если не указан день или месяц
                    schedule.every().day.at(dt.format("HH:mm")).do(
                        job, chat_id, text
                    ).tag(reminder_name)


# Функция для обновления расписания
def update_schedule():
    logging.info(f"Обновление расписания...")
    schedule_messages()


# Функция для логирования запланированных задач
def log_scheduled_jobs():
    jobs = schedule.get_jobs()
    for job in jobs:
        logging.info(f"Запланированная задача: {job}")


@bot.message_handler(commands=["start"])
def start(message: types.Message):
    bot.send_message(message.from_user.id, welcome_message, reply_markup=channelMenu)


@bot.message_handler(content_types=["new_chat_members"])
def on_user_joined(message: types.Message):
    logger.info("New chat member joined: %s", message.new_chat_members)
    params = {
        "chat_id": message.chat.id,
        "chat_title": message.chat.title,
        "user_id": message.from_user.id,
        "status_type": "active",
        "TZ": None,
    }
    try:
        Chat.objects(chat_id=message.chat.id).update(**params, upsert=True)
        logger.info("User %s added to chat %s", message.from_user.id, message.chat.id)
        if not message.reply_to_message:
            bot.reply_to(
                message, "Спасибо за добавление в группу!", reply_markup=channelMenu
            )

    except Exception as e:
        logger.error("Error updating chat database: %s", str(e))


@bot.message_handler(content_types=["left_chat_member"])
def farewell_members(message: types.Message):
    logger.info("Chat member left: %s", message.left_chat_member)
    params = {
        "chat_id": message.chat.id,
        "chat_title": message.chat.title,
        "user_id": message.from_user.id,
        "status_type": "left_chat_member",
    }
    try:
        Chat.objects(chat_id=message.chat.id).update(**params, upsert=True)
        logger.info(
            "User %s removed from chat %s", message.from_user.id, message.chat.id
        )
    except Exception as e:
        logger.error("Error updating chat database: %s", str(e))


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Настройка уровня логирования
    logging.info("Запуск планировщика сообщений")
    update_schedule()  # Первоначальный запуск для планирования

    # Планируем обновление расписания каждые 70 секунд
    schedule.every(20).seconds.do(update_schedule).tag("update_schedule")

    # Запуск планировщика в отдельном потоке
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    # Запуск бота
    bot.infinity_polling()
