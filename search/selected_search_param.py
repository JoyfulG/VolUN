from PyQt6 import QtWidgets, QtCore


class SelectedSearchParam(QtWidgets.QPushButton):
    def __init__(self, option_name):
        super(SelectedSearchParam, self).__init__()

        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)

        self.setText(option_name)
        icon = QtWidgets.QStyle.StandardPixmap.SP_TitleBarCloseButton
        self.setIcon(self.style().standardIcon(icon))

        self.setObjectName('SelectedSearchParam')
        self.setStyleSheet('QPushButton#SelectedSearchParam {'
                           'border-radius: 8px;'
                           'padding: 3px;'
                           'background-color: grey;}')

        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        print('Bubble clicked!')
