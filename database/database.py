from operator import methodcaller
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.models import Group, User, Subject, SubjectItem, Mark

engine = create_engine(f"postgresql://postgres:password@172.18.89.107:5432/journal")


def get_insert_session(data: List[Group | User | Subject | SubjectItem | Mark]):
    with Session(engine, autocommit=True) as session:
        session.add_all(data)


def get_session(statement, return_type=None):
    print(return_type)
    with Session(engine, autocommit=True) as session:
        if return_type is None:
            session.execute(statement)
        else:
            return methodcaller(return_type)(session.execute(statement))
