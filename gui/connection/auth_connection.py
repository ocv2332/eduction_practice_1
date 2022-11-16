from typing import NamedTuple

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from sqlalchemy.exc import NoResultFound

from database.models import Roles, User
from database.queries import get_query_by_auth_data, QueryReturnType
from gui.connection.main_connection import MainWindow
from gui.windows import auth_window


class AuthData(NamedTuple):
    login: str
    password: str


class UserInfo(NamedTuple):
    fio: str
    role: Roles


class AuthWindow(QtWidgets.QMainWindow, auth_window.Ui_AuthWindow):
    def __init__(self):
        super(AuthWindow, self).__init__()

        self.setupUi(self)
        self.login_button.clicked.connect(self.open_main_window)
        self.LOGIN = self.PASSWORD = None

    def _get_auth_data(self) -> AuthData:
        return AuthData(login=self.user_login.text(), password=self.user_password.text())

    @staticmethod
    def _get_user_role_by_auth_data(auth_data: AuthData):
        return Roles(get_query_by_auth_data((User.role,), auth_data.login, auth_data.password, QueryReturnType.one)[0])

    def _hide_admin_widgets(self):
        pass

    @staticmethod
    def _hide_teacher_widgets(window_object):
        window_object.admin_panel_button.hide()

    @staticmethod
    def _hide_student_widgets(window_object):
        window_object.admin_panel_button.hide()
        window_object.scrollArea_groups.hide()

    def _hide_widgets_by_role(self, window_object, role: Roles):
        match role:
            case Roles.admin:
                self._hide_admin_widgets()
            case Roles.teacher:
                self._hide_teacher_widgets(window_object)
            case Roles.student:
                self._hide_student_widgets(window_object)
            case _:
                pass

    def _get_user_info(self, auth_data: AuthData) -> UserInfo:
        user_role = self._get_user_role_by_auth_data(self._get_auth_data())
        user_fio = get_query_by_auth_data((User.last_name, User.first_name, User.middle_name),
                                          auth_data.login, auth_data.password, QueryReturnType.one)

        return UserInfo(user_fio, user_role)

    @staticmethod
    def _fill_user_info_fields(window_object, user_info: UserInfo):
        window_object.user_fio.setText(str(user_info.fio))
        window_object.user_role.setText(f"Роль: {user_info.role}")

    def create_message_box(icon: QMessageBox, title: str, text: str):
        """Метод, изменяющий цвет прогрессбара
            Args:
            icon: Иконка окна
            title: Название окна
            text: Текст ошибки
        """

        msg = QtWidgets.QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        return msg

    def open_main_window(self):
        try:
            user_info = self._get_user_info(self._get_auth_data())
            main_window = MainWindow()
            self._hide_widgets_by_role(main_window, user_info.role)
            self._fill_user_info_fields(main_window, user_info)
            self.close()
            main_window.initilization()
            main_window.show()
        except NoResultFound:
            msg = self.create_message_box(QtWidgets.QMessageBox.Warning, "Ошибка", "Неверный логин или пароль")
            msg.exec_()
