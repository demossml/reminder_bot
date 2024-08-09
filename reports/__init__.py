# reports/__init__.py


# from reports import upload_data

from reports import settings, reminder
from bd.model import Session

user_id = [490899906]


def get_reports(session: Session):
    if session.user_id in user_id:
        return {
            "reminder": reminder,
            "settings": settings,
        }
    else:
        return {
            "reminder": reminder,
        }


reports = {"settings": settings, "reminder": reminder}
