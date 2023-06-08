from PyQt6 import QtWidgets, QtCore


class SelectedSearchParam(QtWidgets.QPushButton):
    def __init__(self, item):
        super(SelectedSearchParam, self).__init__()

        self.item = item

        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)

        icon = QtWidgets.QStyle.StandardPixmap.SP_TitleBarCloseButton
        self.setIcon(self.style().standardIcon(icon))

        self.setObjectName('SelectedSearchParam')
        self.setStyleSheet('QPushButton#SelectedSearchParam {'
                           'border-radius: 8px;'
                           'padding: 3px;'
                           'background-color: grey;}')

        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        pass


class SelectedSearchParamCheckbox(SelectedSearchParam):
    def __init__(self, *args, **kwargs):
        super(SelectedSearchParamCheckbox, self).__init__(*args, **kwargs)

        self.setText(self.item.text())

    def on_clicked(self):
        self.item.setCheckState(QtCore.Qt.CheckState.Unchecked)


class SelectedSearchParamRanged(SelectedSearchParam):
    def __init__(self, *args, **kwargs):
        super(SelectedSearchParamRanged, self).__init__(*args, **kwargs)

        max_length = self.item.itemAt(1).itemAt(3).widget().maxLength()
        self.max_value = 10 ** max_length - 1

        self.title_text = self.item.itemAt(0).widget().text() + ' '
        self.input_from_text = self.item.input_from.text() if self.item.input_from.text() else '0'
        self.input_to_text = self.item.input_to.text() if self.item.input_to.text() else str(self.max_value)

        self.setText(self.title_text + self.input_from_text + ' - ' + self.input_to_text)

    def on_clicked(self):
        self.item.input_from.clear()
        self.item.input_to.clear()
