import sys

from PyQt5 import QtWidgets

from gui.connection.auth_connection import AuthWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
