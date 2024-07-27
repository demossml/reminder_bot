from bd.model import (
    Session,
)


class DocStatusInput:
    """Статус документа -
    open продолжить выбор,
    completed закончить выбор
    """

    desc = "Выберите действие: продолжить или завершить"
    type = "SELECT"

    def get_options(self, session: Session):
        output = (
            {"id": "open", "name": "➕ Добавить ➡️".upper()},
            {"id": "completed", "name": "✅ Завершить ➡️".upper()},
        )
        return output
