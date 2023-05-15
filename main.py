import sys

from PyQt6 import QtWidgets, QtGui, QtCore

from profile import ProfilePicture
from clickable_labels import QLabelClickable
from show_previews import ShowPreviews
from database_handler import DatabaseHandler
from search.search_widget import SearchWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('VolUN')
        self.setWindowIcon(QtGui.QIcon('volun_icon.png'))
        self.resize(1200, 700)
        self.setMinimumSize(500, 350)

        docked_menu = self.docked_menu()
        main_area = self.central_widget()

        self.setCentralWidget(main_area)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, docked_menu)

        self.show()

    @staticmethod
    def central_widget():
        search_widget = SearchWidget()
        previews_widget = ShowPreviews(DatabaseHandler.get_previews_info())

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(search_widget)
        vbox.addWidget(previews_widget)
        cent_widget = QtWidgets.QWidget()
        cent_widget.setLayout(vbox)

        return cent_widget

    @classmethod
    def docked_menu(cls):
        username_label = cls.username_label_docked_menu()
        userpic_label = cls.userpic_label_docked_menu()
        home_option_hbox = cls.docked_menu_option('HOME', cls.temp_func)
        saved_option_hbox = cls.docked_menu_option('SAVED', cls.temp_func)
        search_option_hbox = cls.docked_menu_option('SEARCH', cls.temp_func)

        docked_vbox = QtWidgets.QVBoxLayout()
        docked_vbox.insertSpacing(0, 20)
        docked_vbox.addWidget(userpic_label)
        docked_vbox.insertSpacing(2, 10)
        docked_vbox.addWidget(username_label)
        docked_vbox.insertSpacing(4, 50)
        docked_vbox.addLayout(home_option_hbox)
        docked_vbox.insertSpacing(6, 10)
        docked_vbox.addLayout(saved_option_hbox)
        docked_vbox.insertSpacing(8, 10)
        docked_vbox.addLayout(search_option_hbox)
        docked_vbox.addStretch()

        docked_label = QtWidgets.QLabel()
        docked_label.setLayout(docked_vbox)

        docked_menu = QtWidgets.QDockWidget()
        docked_menu.setFixedWidth(280)
        docked_menu.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        docked_menu.setTitleBarWidget(QtWidgets.QWidget())  # Getting rid of the docked_menu title bar.
        docked_menu.setWidget(docked_label)

        return docked_menu

    @staticmethod
    def userpic_label_docked_menu():
        userpic = ProfilePicture('test_pp.jpg', 150)
        userpic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        return userpic

    @staticmethod
    def username_label_docked_menu():
        name = 'TestUsername'
        name_label = QtWidgets.QLabel()
        name_label.setText(f'<b>{name}</b>')
        name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        name_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        name_label.setFont(QtGui.QFont('Arial', 16))

        return name_label

    @staticmethod
    def docked_menu_option(name, func):
        option_label = QLabelClickable(func)
        option_label.setText(f'<b>{name}<b/>')
        option_label.setFont(QtGui.QFont('Arial', 20))
        option_hbox = QtWidgets.QHBoxLayout()
        option_hbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        option_hbox.addWidget(option_label)
        option_hbox.insertSpacing(0, 30)

        return option_hbox

    @staticmethod
    def temp_func():
        print('Clicked!')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
