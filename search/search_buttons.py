from PyQt6 import QtWidgets, QtCore


class StartSearchButton(QtWidgets.QPushButton):
    def __init__(self):
        super(StartSearchButton, self).__init__()

        self.setText('SEARCH')
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setMinimumWidth(120)
        self.setStyleSheet('QPushButton { border: none; padding: 5px; border-radius: 8px; background-color: #70e7a2; }')


class ClearAllButton(QtWidgets.QPushButton):
    def __init__(self):
        super(ClearAllButton, self).__init__()

        self.setText('CLEAR ALL')
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setMinimumWidth(120)
        self.setStyleSheet('QPushButton { border: none; padding: 5px; border-radius: 8px; background-color: #bcbcbc; }')
