from enum import Enum
from itertools import chain
from typing import List

from sqlalchemy import select

from database.database import get_session
from database.models import Roles, User, Group


class QueryReturnType(Enum):
    one = "one"
    all = "all"


def _align_list(lst: List[tuple]):
    return list(chain.from_iterable(lst))


def _get_sorted_sequence(sequence: List[tuple]):
    return sorted(_align_list(sequence))


def get_query_by_auth_data(fields: tuple, login: str, password: str, return_type: QueryReturnType):
    return get_session(select(*fields).where(User.login == login, User.password == password), return_type.value)


def get_last_index(field_table_id):
    return _get_sorted_sequence(get_session(select(field_table_id), "all"))[-1]


def get_group_names():
    return _get_sorted_sequence(get_session(select(Group.title), "all"))


def get_user_by_role(fields: tuple, role: Roles, return_type: QueryReturnType):
    return sorted(
        [' '.join(result) for result in get_session(select(*fields).where(User.role == role), return_type.value)])


def get_user_by_auth_data(fields: tuple, login: str, password: str):
    return sorted([' '.join(index) for index in get_query_by_auth_data(fields, login, password, QueryReturnType.all)])


def get_id_by_user_role_and_fio(role: Roles, user_fio, return_type: QueryReturnType = QueryReturnType.one):
    return get_session(select(User.user_id).where(User.role == role.value,
                                                  User.last_name == user_fio.lastName,
                                                  User.first_name == user_fio.firstName,
                                                  User.middle_name == user_fio.middleName), return_type.value)[0]


def get_id_by_name(field_table_id, field_table_name, comparable_name, return_type: QueryReturnType = QueryReturnType.one):
    return get_session(select(field_table_id).where(field_table_name == comparable_name), return_type.value)[0]


def get_name_by_id(field_table_id, field_table_name, comparable_id, return_type: QueryReturnType = QueryReturnType.one):
    return get_session(select(field_table_name).where(field_table_id == comparable_id), return_type.value)[0]


def get_fields_using_single_comparison(fields: tuple, left_value, right_value, return_type: QueryReturnType):
    return get_session(select(*fields).where(left_value == right_value), return_type.value)
