from PyQt6 import QtCore, QtGui, QtWidgets

from database_handler import DatabaseHandler


class InitiateSearch(QtWidgets.QWidget):
    def __init__(self):
        super(InitiateSearch, self).__init__()

        self.toggle_button = QtWidgets.QToolButton()
        self.toggle_button.setCheckable(True)
        self.toggle_button.setObjectName('InitiateSearchWidgetToggleButton')
        self.toggle_button.setStyleSheet('QToolButton#InitiateSearchWidgetToggleButton { border: none; }')
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.ArrowType.DownArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.content_area = QtWidgets.QScrollArea()
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)
        self.content_area.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.content_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        vbox = QtWidgets.QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.toggle_button)
        vbox.addWidget(self.content_area)
        self.setLayout(vbox)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b'minimumHeight'))
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self, b'maximumHeight'))
        self.toggle_animation.addAnimation(QtCore.QPropertyAnimation(self.content_area, b'maximumHeight'))

    def set_content_layout(self, layout):
        self.content_area.setLayout(layout)
        collapsed_height = (self.sizeHint().height() - self.content_area.maximumHeight())
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

    @QtCore.pyqtSlot()
    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(QtCore.Qt.ArrowType.UpArrow if not checked else QtCore.Qt.ArrowType.DownArrow)
        self.toggle_animation.setDirection(
            QtCore.QAbstractAnimation.Direction.Forward
            if not checked
            else QtCore.QAbstractAnimation.Direction.Backward
        )
        self.toggle_animation.start()


class SearchParam(QtWidgets.QWidget):
    def __init__(self, group_title, db_column):
        super(SearchParam, self).__init__()

        title_label = QtWidgets.QLabel(group_title)
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        options_widget = SearchParamOptions(db_column)

        group_vbox = QtWidgets.QVBoxLayout()
        group_vbox.addWidget(title_label)
        group_vbox.addWidget(options_widget)

        self.setLayout(group_vbox)


class SearchParamOptions(QtWidgets.QListWidget):
    def __init__(self, db_column_from_parent):
        super(SearchParamOptions, self).__init__()

        self.setSortingEnabled(True)

        group_options = DatabaseHandler.get_distinct_values(db_column_from_parent)
        for option_name in group_options:
            listitem = QtWidgets.QListWidgetItem(option_name)
            listitem.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.addItem(listitem)

        self.itemPressed.connect(self.toggle_item)

    def toggle_item(self, item):
        if not item:  # Check later if this condition is needed here at all
            return
        if item.checkState() == QtCore.Qt.CheckState.Checked:
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.CheckState.Checked)


class SelectedSearchOption(QtWidgets.QPushButton):
    def __init__(self, option_name):
        super(SelectedSearchOption, self).__init__()

        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)

        self.setText(option_name)
        icon = QtWidgets.QStyle.StandardPixmap.SP_TitleBarCloseButton
        self.setIcon(self.style().standardIcon(icon))

        self.setObjectName('SelectedSearchOption')
        self.setStyleSheet('QPushButton#SelectedSearchOption {'
                           'border-radius: 8px;'
                           'padding: 3px;'
                           'background-color: grey;}')

        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        print('HIHI HAHA')


if __name__ == "__main__":
    import sys
    import random

    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QMainWindow()
    w.setCentralWidget(SearchParam('Territory', 'territory'))
    dock = QtWidgets.QDockWidget("Collapsible Demo")
    w.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, dock)
    scroll = QtWidgets.QScrollArea()
    dock.setWidget(scroll)
    content = QtWidgets.QWidget()
    scroll.setWidget(content)
    scroll.setWidgetResizable(True)
    vlay = QtWidgets.QVBoxLayout(content)
    for a in range(10):
        box = InitiateSearch()
        box.toggle_button.setText('SEARCH')
        vlay.addWidget(box)
        lay = QtWidgets.QVBoxLayout()
        for b in range(8):
            labell = QtWidgets.QLabel("{}".format(b))
            color = QtGui.QColor(*[random.randint(0, 255) for _ in range(3)])
            labell.setStyleSheet(
                "background-color: {}; color : white;".format(color.name())
            )
            labell.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            lay.addWidget(labell)

        box.set_content_layout(lay)

    selected_grid = QtWidgets.QGridLayout()
    selected_grid.addWidget(SelectedSearchOption('OOOO'))
    selected_grid.addWidget(SelectedSearchOption('1111'))
    vlay.addLayout(selected_grid)
    vlay.addStretch()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec())
