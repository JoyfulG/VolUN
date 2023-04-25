from PyQt6 import QtCore, QtGui, QtWidgets

from database_handler import DatabaseHandler


class InitiateSearch(QtWidgets.QWidget):
    def __init__(self):
        super(InitiateSearch, self).__init__()

        self.toggle_button = QtWidgets.QToolButton()
        self.toggle_button.setCheckable(True)
        self.toggle_button.setObjectName('SearchParamsWidgetToggleButton')
        self.toggle_button.setStyleSheet('QToolButton#SearchParamsWidgetToggleButton { border: none; }')
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.ArrowType.DownArrow)
        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

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


class SearchParamGroup(QtWidgets.QWidget):
    def __init__(self, group_title, db_column):
        super(SearchParamGroup, self).__init__()

        title_label = QtWidgets.QLabel(group_title)
        reset_button = QtWidgets.QLabel('RESET')
        title_and_reset_hbox = QtWidgets.QHBoxLayout()
        title_and_reset_hbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_and_reset_hbox.addWidget(title_label)
        title_and_reset_hbox.addWidget(reset_button)

        options_box = self.create_options_box(db_column)

        group_vbox = QtWidgets.QVBoxLayout()
        group_vbox.addLayout(title_and_reset_hbox)
        group_vbox.addWidget(options_box)

        self.setLayout(group_vbox)

    @staticmethod
    def create_options_box(db_column_from_init):
        """
        checked чекбоксы перемещать вверх
        """

        scroll_area_widget_vbox = QtWidgets.QVBoxLayout()
        group_options = DatabaseHandler.get_distinct_values(db_column_from_init)
        for option_name in group_options:
            option_checkbox = QtWidgets.QCheckBox(option_name)
            scroll_area_widget_vbox.addWidget(option_checkbox)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area_widget = QtWidgets.QWidget()
        scroll_area_widget.setLayout(scroll_area_widget_vbox)
        scroll_area.setWidget(scroll_area_widget)

        return scroll_area


if __name__ == "__main__":
    import sys
    import random

    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QMainWindow()
    w.setCentralWidget(SearchParamGroup('Host entity', 'host_entity'))
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
            label = QtWidgets.QLabel("{}".format(b))
            color = QtGui.QColor(*[random.randint(0, 255) for _ in range(3)])
            label.setStyleSheet(
                "background-color: {}; color : white;".format(color.name())
            )
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            lay.addWidget(label)

        box.set_content_layout(lay)
    vlay.addStretch()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec())
