# reports/__init__.py

from reports import download_data


# from reports import upload_data

from reports import pdf_to_xls
from bd.model import Session

user_id = [49089990677]
timur_id = [301477504, 490899906]


def get_reports(session: Session):
    if session.user_id in user_id:
        return {
            "pdf_to_xls": pdf_to_xls,
        }


reports = {
    "pdf_to_xls": pdf_to_xls,
}
