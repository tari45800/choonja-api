from sqlalchemy.orm import Session
from app.utils.parser.extract_parts import extract_parts
from app.crud.action import find_action
from app.crud.schedule import delete_d_days

# 서비스 로직
def delete_d_day_service(text: str, db: Session):
    parsed = extract_parts(text)
    if 'result' in parsed:
        return parsed  

    an = parsed['action']

    return delete_d_days(an, db)