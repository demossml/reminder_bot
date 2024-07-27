from bd.model import (
    Session,
    Chat,
)

from .inputs import DocStatusInput


from arrow import utcnow, get

import logging

logger = logging.getLogger(__name__)

from pprint import pprint

name = "🛠 Настройки ➡️".upper()
desc = ""
mime = "text"


class ReportsSettingsInput:
    """
    Меню настроек бота
    """

    name = "Выберете".upper()
    desc = "Выберете".upper()
    type = "SELECT"

    def get_options(self, session: Session):
        output = ({"id": "chat", "name": "Чаты ➡️".upper()},)
        return output


class ReportsSettingsChatInput:
    """
    Меню настроек бота
    """

    name = "Выберете".upper()
    desc = "Выберете".upper()
    type = "SELECT"

    def get_options(self, session: Session):
        output = [
            {"id": "add_chat", "name": "➕ ДОБАВИТЬ ЧАТ ➡️"},
            {"id": "delete_chat", "name": "− УДАЛИТЬ ЧАТ ➡️"},
            {"id": "view_chats", "name": "👀 ПРОСМОТРЕТЬ ЧАТЫ ➡️"},
        ]
        return output


class LinkInput:
    desc = "Напишите адрес формате @chat_name ✍️".upper()
    type = "MESSAGE"


class GetLinInput:
    """
    Класс для получения списка чатов
    """

    desc = "Выберите чат"
    type = "SELECT"

    def get_options(self, session: Session):
        output = []

        room = session["room"]
        # pprint(room)
        data_link = []
        # содоет ключи в session.params["inputs"]
        for i in range(int(room) + 1):
            # если в 'link' есть в session.params["inputs"][str(i)]
            if "link" in session.params["inputs"][str(i)]:
                # если 'link' нет в словаре с ключем i в списке data_link
                if session.params["inputs"][str(i)]["link"] not in data_link:

                    # добовляет 'link' в список data_link
                    data_link.append(session.params["inputs"][str(i)]["link"])

        for item in Chat.objects(user_id=session.user_id, status_type="active"):
            if item["link"] not in data_link:
                output.append({"id": item["link"], "name": item["link"]})

        return output


def get_inputs(session: Session):
    inputs = session.params.get("inputs", {}).get("0", {})

    if not inputs:
        return {
            "report": ReportsSettingsChatInput,
        }

    report_type = inputs.get("report", None)

    if report_type == "add_chat":
        return {
            "link": LinkInput,
            "docStatus": DocStatusInput,
        }

    elif report_type == "delete_chat":

        return {
            "link": GetLinInput,
            "docStatus": DocStatusInput,
        }
    elif report_type == "view_chats":

        return {}


def generate(session: Session):
    inputs = session.params.get("inputs", {}).get("0", {})
    pprint(session.user_id)
    report_type = inputs.get("report", None)
    room = session["room"]
    if report_type == "add_chat":
        report_data = []
        # содоет ключи в session.params["inputs"]
        for i in range(int(room) + 1):
            # Добавляем "shop_id" в список shop_ids
            params = session.params["inputs"][str(i)]
            params.update(
                {
                    "user_id": session.user_id,
                    "status_type": "active",
                    "date": utcnow().to("local").isoformat(),
                }
            )

            Chat.objects(link=params["link"]).update(**params, upsert=True)

            report_data.append(
                {"АДРЕС:": params.get("link", "Не указан"), "СТАТУС:": "ДОБАВЛЕН"}
            )
        return report_data
    if report_type == "delete_chat":
        report_data = []
        # содоет ключи в session.params["inputs"]
        for i in range(int(room) + 1):
            params = session.params["inputs"][str(i)]
            params.update(
                {
                    "user_id": session.user_id,
                    "status_type": "delete",
                    "date": utcnow().to("local").isoformat(),
                }
            )

            Chat.objects(user_id=session.user_id, link=params["link"]).update(
                **params, upsert=True
            )

            report_data.append(
                result={"АДРЕС": params.get("link", "Не указан"), "СТАТУС": "УДАЛЕН"}
            )
        return report_data
    if report_type == "view_chats":
        report_data = []
        for item in Chat.objects(user_id=session.user_id):

            report_data.append(
                {
                    "АДРЕС": item["link"],
                    "ДАТА": item["date"],
                    "СТАТУС": item["status_type"],
                }
            )

        return report_data
