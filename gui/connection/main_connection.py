from itertools import chain
from typing import NamedTuple, List

import pandas as pd
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QPushButton
from sqlalchemy import select

from database import models
from database.database import get_session, get_insert_session
from database.models import User, Group, Subject, Roles, SubjectItem
from database.queries import get_last_index, QueryReturnType, get_id_by_name, get_id_by_user_role_and_fio, \
    get_fields_using_single_comparison, get_name_by_id, get_user_by_role
from gui.pyqt.tablemodel import TableModel
from gui.windows import main_window


class Properties(NamedTuple):
    widget: QWidget
    name: str
    content: str
    left: int
    top: int
    width: int
    height: int
    font: str = "Microsoft YaHei"
    fontSize: int = 8
    grid_x: int = None
    grid_y: int = None
    stylesheet: str = None


class GroupInfo(NamedTuple):
    lastIndex: int
    title: str


class UserFio(NamedTuple):
    lastName: str
    firstName: str
    middleName: str


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)
        self.add_user_button.clicked.connect(self.add_user)
        self.add_group_button.clicked.connect(self.add_group)
        self.add_subject_button.clicked.connect(self.add_subject)
        self.subject_items_add_button.clicked.connect(self.add_event_page)

        self.buttons_group = []
        self.buttons_subject_table = []
        self.buttons_subject_event = []
        self.buttons_subject_diagram = []

        self.group_name = self.subject_id = None

        self.stackedWidget.setCurrentIndex(0)

    def initilization(self):
        self.check_dynamic_button_group()

        for i in range(len(self.buttons_group)):
            self.buttons_group[i].clicked.connect(self.check_dynamic_button_table)
    @staticmethod
    def _get_button_base(properties: Properties) -> QPushButton:
        button = QtWidgets.QPushButton(properties.widget)
        button.setGeometry(QtCore.QRect(properties.left, properties.top, properties.width, properties.height))
        button.setMinimumHeight(properties.height)
        button.setMaximumHeight(properties.height)
        button.setMaximumWidth(properties.width)
        button.setMinimumWidth(properties.width)
        button.setText(properties.content)
        button.setFont(QtGui.QFont(properties.font, properties.fontSize))
        button.setObjectName(properties.name)

        return button

    def _add_button_table(self, properties: Properties):
        button = self._get_button_base(properties)
        self.gridLayout.addWidget(button, properties.grid_x, properties.grid_y, 1, 1)
        return button

    def _add_button_group(self, properties: Properties) -> QPushButton:
        button = self._get_button_base(properties)
        self.verticalLayout.addWidget(button)
        return button

    def _add_button_event(self, properties: Properties):
        button = self._get_button_base(properties)
        button.setStyleSheet(properties.stylesheet)
        self.gridLayout.addWidget(button, properties.grid_y, properties.grid_y, 1, 1)
        return button

    def add_user(self):
        user_info = {
            "group_id": get_id_by_name(models.Group.group_id, models.Group.title, self.add_user_group.currentText(),
                                       QueryReturnType.one),
            "first_name": self.add_user_first_name.text(),
            "last_name": self.add_user_last_name.text(),
            "middle_name": self.add_user_middle_name.text(),
            "birthday": self.add_user_calendar.selectedDate().toString("yyyy-MM-dd"),
            "email": self.add_user_email.text(),
            "login": self.add_user_login.text(),
            "password": self.add_user_password.text(),
            "role": self.add_user_password.currentText()
        }

        get_insert_session(User(**user_info))
        self.stackedWidget.setCurrentIndex(0)

    def _get_group_info(self) -> GroupInfo:
        title = self.add_group_name.text()
        last_index = get_last_index(models.Group.group_id) + 1

        return GroupInfo(last_index, title)

    def add_group(self):
        group_info = self._get_group_info()
        self._add_button_group(Properties(self.scrollArea_groups_contents, "push_1", group_info.title,
                                          10, group_info.lastIndex * 30, 351, 23))
        get_insert_session(Group(title=group_info.title))
        self.stackedWidget.setCurrentIndex(0)

    def add_subject(self):
        subject_info = {
            "teacher_id": get_id_by_user_role_and_fio(Roles.teacher,
                                                      UserFio(*self.add_subject_teacher.currentText().split())),
            "group_id": get_id_by_name(models.Group.group_id, models.Group.title, self.add_subject_group.currentText()),
            "title": self.add_subject_name.text()
        }

        get_insert_session(Subject(**subject_info))
        self.stackedWidget.setCurrentIndex(0)

    def add_event_page(self):
        event_info = {
            "subject_id": int(self.subject_id),
            "title": self.subject_items_name.text(),
            "date_event": self.subject_items_calendar.selectedDate().toString("yyyy-MM-dd"),
            "comment": self.subject_items_comment.toPlainText(),
            "max_mark": int(self.subject_items_maxMark_lineEdit.text())
        }

        get_insert_session(SubjectItem(**event_info))
        self.stackedWidget.setCurrentIndex(0)

    def check_dynamic_button_table(self):
        sender = self.sender()
        self.group_name = sender.text()
        group_id = \
            get_fields_using_single_comparison(Group.group_id, Group.title, self.group_name, QueryReturnType.one)[0]
        subject = get_fields_using_single_comparison(Subject.title, Subject.group_id, group_id, QueryReturnType.all)

        for i in range(0, len(subject)):
            group_id = \
                get_fields_using_single_comparison(Group.group_id, Group.title, self.group_name, QueryReturnType.one)[
                    0]
            title_subject = \
                get_fields_using_single_comparison(Subject.title, Subject.group_id, group_id, QueryReturnType.one)[0]
            subject_id = \
                get_fields_using_single_comparison(Subject.subject_id, Subject.title, title_subject,
                                                   QueryReturnType.one)[0]

            self.buttons_subject_table.append(
                self._add_button_table(Properties(self.scrollArea_subjects_contents, f"push_1_{i}", title_subject,
                                                  10, (i * 35), 283, 23, grid_x=i, grid_y=0)))
            self.buttons_subject_event.append(self._add_button_event(Properties(self.scrollArea_subjects_contents,
                                                                                f"push_{subject_id}", str(subject_id),
                                                                                10, (i * 35), 24, 24, grid_x=i,
                                                                                grid_y=1)))
            self.buttons_subject_diagram.append(self._add_button_event(Properties(self.scrollArea_subjects_contents,
                                                                                  f"push_{subject_id}", str(subject_id),
                                                                                  10, (i * 35), 24, 24, grid_x=i,
                                                                                  grid_y=2)))

            for digit in range(len(self.buttons_subject_table)):
                self.buttons_subject_table[digit].clicked.connect(self.show_table)

            for digit in range(len(self.buttons_subject_table)):
                self.buttons_subject_event[digit].clicked.connect(self.trans_event_page)

    def trans_event_page(self):
        sender = self.sender()
        self.subject_id = sender.text()
        self.stackedWidget.setCurrentIndex(2)

    @staticmethod
    def _align_list(lst: List[tuple]):
        return list(chain.from_iterable(lst))

    def show_table(self):
        sender = self.sender()
        title_subject = sender.text()

        get_group_id = get_session(select(models.Group.group_id).where(models.Group.title == self.group_name),
                                   'one')[0]
        get_subject_id = get_session(select(models.Subject.subject_id).where(models.Subject.title == title_subject),
                                     'one')[0]
        get_item_id = get_session(
            select(models.SubjectItem.item_id).where(models.SubjectItem.subject_id == get_subject_id), 'one')[0]
        get_all_student = get_session(
            select(models.User.last_name).where(models.User.role == 'student' and models.User.group_id == get_group_id),
            'all')
        get_all_date = get_session(
            select(models.SubjectItem.date_event).where(models.SubjectItem.subject_id == get_subject_id), 'all')
        get_all_marks = get_session(select(models.Mark.mark).where(models.Mark.item_id == get_item_id), 'all')

        date_lenght = len(get_all_date)

        data = pd.DataFrame(
            [[*self._align_list(get_all_marks[index * date_lenght:(index + 1) * date_lenght])] for index in
             range(len(self._align_list(get_all_student)))], columns=self._align_list(get_all_date),
            index=self._align_list(get_all_student))

        model = TableModel(data)
        self.table.setModel(model)

    def check_dynamic_button_group(self):
        last_index_group = get_last_index(Group.group_id)

        match self.user_role.text()[6:]:
            case "Roles.admin":
                for i in range(0, int(last_index_group) - 1):
                    title = get_name_by_id(Group.group_id, Group.title, i + 1, QueryReturnType.one)
                    self.buttons_group.append(
                        self._add_button_group(Properties(self.scrollArea_groups_contents, f"push_{i}",
                                                          title, 10, (i * 30), 51,
                                                          23)))
            case "Roles.teacher":
                for i in range(0, int(last_index_group)):
                    teacher_id = get_user_by_role(User.user_id, Roles.teacher, QueryReturnType.one)[0]
                    group_teacher_id = get_fields_using_single_comparison(Subject.group_id, Subject.teacher_id,
                                                                          teacher_id, QueryReturnType.all)
                    group_title = get_fields_using_single_comparison(Group.title, Group.group_id, group_teacher_id,
                                                                     QueryReturnType.all)

                    self.buttons_group.append(self._add_button_group(Properties(self.scrollArea_groups_contents,
                                                                                f"push_{i}", group_title, 10, (i * 30),
                                                                                351, 23)))
            case _:
                pass
