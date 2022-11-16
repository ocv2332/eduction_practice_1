from collections import namedtuple
from typing import NamedTuple, List

from database.models import Roles
from database.models import User
from database.queries import get_group_names, get_user_by_role, QueryReturnType


class AdminPanelData(NamedTuple):
    groupNames: List[str]
    users: List[str]


PropertyData = namedtuple("PropertyData", ["object", "func"])


def _execute_property(properties: tuple):
    for property_ in properties:
        property_.object.clear()
        property_.object.addItems(property_.func)


def _prepare_data_admin_panel() -> AdminPanelData:
    group_names = get_group_names()
    users = get_user_by_role((User.last_name, User.first_name, User.middle_name), Roles.teacher, QueryReturnType.all)

    return AdminPanelData(groupNames=group_names, users=users)


def initialization_admin_panel(object_windows):
    admin_panel_data = _prepare_data_admin_panel()

    admin_panel_settings = (
        PropertyData(object=object_windows.add_user_role, func=["Роли"].extend(Roles.list())),
        PropertyData(object=object_windows.add_user_group, func=["Группа"].extend(admin_panel_data.groupNames)),
        PropertyData(object=object_windows.add_subject_group, func=["Группы"].extend(admin_panel_data.groupNames)),
        PropertyData(object=object_windows.add_subject_teacher, func=["Роли"].extend(admin_panel_data.users))
    )

    _execute_property(admin_panel_settings)
    object_windows.stackedWidget.setCurrentIndex(1)
