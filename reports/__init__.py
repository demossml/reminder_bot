# reports/__init__.py


# from reports import upload_data

from reports import settings, reminder
from bd.model import Session

user_id = [49089990677]


def get_reports(session: Session):
    return {"settings": settings, "reminder": reminder}


reports = {"settings": settings, "reminder": reminder}
