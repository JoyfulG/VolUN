import sys

from PyQt6 import QtWidgets, QtGui, QtCore

from profile import ProfilePicture


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('VolUN')
        self.setWindowIcon(QtGui.QIcon('volun_icon.png'))
        self.resize(1200, 700)
        self.setMinimumSize(500, 350)

        docked_menu = self.main_window_docked_menu(self)

        self.setCentralWidget(QtWidgets.QTextEdit())
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, docked_menu)

        self.show()

    @staticmethod
    def main_window_docked_menu(self):
        username_label = self.username_docked_menu_label()
        userpic_label = self.userpic_docked_menu_label()
        home_button = self.home_button_docked_menu()

        docked_vbox = QtWidgets.QVBoxLayout()
        docked_vbox.insertSpacing(0, 20)
        docked_vbox.addWidget(userpic_label)
        docked_vbox.insertSpacing(2, 10)
        docked_vbox.addWidget(username_label)
        docked_vbox.insertSpacing(4, 50)
        docked_vbox.addWidget(home_button)
        docked_vbox.addStretch()

        docked_label = QtWidgets.QLabel()
        docked_label.setLayout(docked_vbox)

        docked_menu = QtWidgets.QDockWidget()
        docked_menu.setFixedWidth(330)
        docked_menu.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        docked_menu.setTitleBarWidget(QtWidgets.QWidget())  # Getting rid of the docked_menu title bar.
        docked_menu.setWidget(docked_label)

        return docked_menu

    @staticmethod
    def userpic_docked_menu_label():
        userpic = ProfilePicture('test_pp.jpg', 150)
        userpic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        return userpic

    @staticmethod
    def username_docked_menu_label():
        name = 'TestUsername'
        name_label = QtWidgets.QLabel()
        name_label.setText(f'<b>{name}</b>')
        name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        name_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        name_label.setFont(QtGui.QFont('Arial', 16))

        return name_label

    @staticmethod
    def home_button_docked_menu():
        button = QtWidgets.QPushButton('Home')

        return button


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
