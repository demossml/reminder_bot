from typing import Callable
from enum import Enum
import telebot
from telebot import types
from arrow import utcnow

from pprint import pprint
import mimetypes
import os
import sys  # Импортируем модуль sys для получения информации о текущем исключении
import asyncio
import time
import io


from bd.model import Message, Session, PDFFile
from reports import reports, get_reports
from util_s import (
    format_message_list5,
    format_message_list4,
)

import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


# стадии сесии
class State(str, Enum):
    INIT = "INIT"
    MENU = "MENU"
    INPUT = "INPUT"
    REPLY = "REPLY"
    READY = "READY"


#
async def handle_message(bot: telebot.TeleBot, message: Message, session: Session):
    start = ["Menu", "/start", "Меню"]
    if message.text in start:
        session.state = State.INIT
        session.room = "0"
        session.update(room=session.room, state=session.state)
    if message.text == "/log":
        text_file_path = "bot.log"
        with open(text_file_path, "rb") as text_file:
            await bot.send_document(message.chat_id, document=text_file)

    next = lambda: handle_message(bot, message, session)
    try:
        await states[session.state](bot, message, session, next)
    except Exception as e:
        # print(ex)
        # raise ex
        logger.exception("Error handling message")
        logger.error(f"Ошибка: {e} на строке {sys.exc_info()[-1].tb_lineno}")
        await bot.send_message(
            message.chat_id, f"Ошибка: {e} на строке {sys.exc_info()[-1].tb_lineno}"
        )
        session.state = State.INIT
        next()


async def handle_init_state(
    bot: telebot.TeleBot, message: Message, session: Session, next: Callable
):

    start_menu = types.InlineKeyboardMarkup(row_width=2)
    for name, report in get_reports(session).items():
        button = types.InlineKeyboardButton(report.name, callback_data=name)
        start_menu.add(button)
    # await bot.delete_message(message.chat_id, message.message_id)
    await bot.send_message(message.chat_id, "Привет", reply_markup=start_menu)
    room = session.room
    session.params = {"inputs": {room: {}}}

    session.state = State.MENU
    session.update(params=session.params, state=session.state)
    logger.debug(f"Handled init state for chat {message.chat_id}")

    # session.save()


async def handle_menu_state(
    bot: telebot.TeleBot, message: Message, session: Session, next: Callable
):
    session.params["report"] = message.text
    session.state = State.INPUT
    session.update(state=session.state, params=session.params)
    logger.debug(f"Handled init state for chat {message.chat_id}")
    await next()


async def handle_input_state(bot, message, session, next):
    report = reports[session.params["report"]]
    # print(report.get_inputs(session).items())
    for name, Input in report.get_inputs(session).items():
        # print(name)
        room = session.room
        if name not in session.params["inputs"][room]:
            session.params["input"] = name
            session.update(params=session.params)
            input = Input()
            if input.type == "SELECT":
                markup = types.InlineKeyboardMarkup(row_width=2)
                options = input.get_options(session)  # [{}, {}, {}, ...]
                for option in options:  # [({}, 0), ({}, 1), ({}, 2)]
                    button = types.InlineKeyboardButton(
                        option["name"], callback_data=option["id"]
                    )
                    markup.add(button)
            if input.type == "LOCATION":
                options = input.get_options(session)  # [{}, {}, {}, ...]
                print(options[0]["name"])
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn_address = types.KeyboardButton(
                    options[0]["name"], request_location=True
                )
                markup.add(btn_address)
            if input.type == "PHOTO":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn_address = types.KeyboardButton("Меню")
                markup.add(btn_address)
                await bot.send_message(message.chat_id, input.desc, reply_markup=markup)
            if input.type == "FILE":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn_address = types.KeyboardButton("Меню")
                markup.add(btn_address)
                await bot.send_message(message.chat_id, input.desc, reply_markup=markup)
            if input.type == "MESSAGE":
                await bot.delete_message(message.chat_id, message.message_id)
                await bot.send_message(message.chat_id, input.desc)
            if input.type == "SELECT":
                await bot.delete_message(message.chat_id, message.message_id)
                await bot.send_message(message.chat_id, input.desc, reply_markup=markup)
            if input.type == "LOCATION":
                await bot.delete_message(message.chat_id, message.message_id)
                await bot.send_message(message.chat_id, input.desc, reply_markup=markup)
            session.state = State.REPLY
            session.update(state=session.state)

            logger.debug(f"Handled init state for chat {message.chat_id}")

            return

    session.state = State.READY
    session.update(state=session.state)
    # session.save()
    await next()


async def handle_reply_state(bot, message, session, next):
    input_name = session.params["input"]
    room = session.room
    if message.text == "open":
        session.room = str(int(session.room) + 1)
        session.params["inputs"][session.room] = {}
        session.update(params=session.params, room=session.room)
    if str(room) not in session.params["inputs"]:
        session.params["inputs"][str(room)] = {}
        session.update(params=session.params)

    session.params["inputs"][str(room)][input_name] = message.text
    session.update(params=session.params)
    # session.params["inputs"][input_name] = message.text

    if message.location:
        session.params["inputs"][str(room)][input_name] = utcnow().now().isoformat()
        session.params["inputs"][str(room)][input_name] = {}
        session.params["inputs"][str(room)][input_name]["data"] = (
            utcnow().now().isoformat()
        )
        session.params["inputs"][str(room)][input_name][
            "lat"
        ] = message.location.latitude
        session.params["inputs"][str(room)][input_name][
            "lon"
        ] = message.location.longitude
        session.update(params=session.params)

    if message.photo:
        session.params["inputs"][str(room)][input_name] = {}
        session.params["inputs"][str(room)][input_name]["photo"] = message.photo[
            -1
        ].file_id
        session.update(params=session.params)

    session.state = State.INPUT
    session.update(params=session.params, state=session.state)
    logger.debug(f"Handled init state for chat {message.chat_id}")
    await next()


async def handle_ready_state(bot, message, session, next):
    report = reports[session.params["report"]]
    result = report.generate(session)

    messages = format_message_list4(result)
    [
        await bot.send_message(message.chat_id, m, parse_mode="MarkdownV2")
        for m in messages
    ]
    session.state = State.INIT
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_address = types.KeyboardButton("Меню")
    markup.add(btn_address)
    await bot.delete_message(message.chat_id, message.message_id)
    await bot.send_message(message.chat_id, "Привет", reply_markup=markup)
    session.update(state=session.state)
    logger.debug(f"Handled ready state for chat {message.chat_id}")

    # session.save()
    # await next()


states = {
    State.INIT: handle_init_state,
    State.MENU: handle_menu_state,
    State.INPUT: handle_input_state,
    State.REPLY: handle_reply_state,
    State.READY: handle_ready_state,
}
