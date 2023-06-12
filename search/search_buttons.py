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
        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        selected_options = self.parent().parent().layout().itemAt(2).widget()
        current_quantity = selected_options.layout.count()
        for index in reversed(range(current_quantity)):
            layout_item = selected_options.layout.itemAt(index)
            if type(layout_item.widget()).__name__ == 'SelectedSearchParamRanged':
                layout_item.widget().item.input_from.setText('')
                layout_item.widget().item.input_to.setText('')
            elif type(layout_item.widget()).__name__ == 'SelectedSearchParamCheckbox':
                layout_item.widget().item.setCheckState(QtCore.Qt.CheckState.Unchecked)
