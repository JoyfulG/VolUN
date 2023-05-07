from PyQt6 import QtCore, QtWidgets

from database_handler import DatabaseHandler


class SearchFilters(QtWidgets.QWidget):
    def __init__(self):
        super(SearchFilters, self).__init__()

        self.toggle_button = QtWidgets.QToolButton()
        self.toggle_button.setText('SEARCH FILTERS')
        self.toggle_button.setCheckable(True)
        self.toggle_button.setStyleSheet('QToolButton { border: none; }')
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.ArrowType.DownArrow)
        self.toggle_button.pressed.connect(self.on_toggle_button_pressed)

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

        self.set_content_layout()

    def set_content_layout(self):
        content_layout = QtWidgets.QGridLayout()
        search_param_lists = [
            ('Host entity', 'host_entity', 'assignments', 0, 0),
            ('Territory', 'territory', 'assignments', 0, 1),
            ('Duty stations', 'station', 'dutystations', 0, 2),
            ('Languages', 'lang', 'languages', 0, 3),
            ('Volunteer category', 'vol_category', 'assignments', 1, 0),
            ('Level of education', 'ed_lvl', 'assignments', 1, 1)
        ]

        for title, db_column, db_table, pos_row, pos_column in search_param_lists:
            search_param_list = SearchParamList(title, db_column, db_table)
            content_layout.addWidget(search_param_list, pos_row, pos_column)

        status_param = SearchParamStatus()

        age_param = SearchParamRanged('Age:', 30, 2)
        duration_param = SearchParamRanged('Duration:', 40, 4)
        published_param = SearchParamRanged('Assignment\npublished:', 100, 10)

        search_params_additional = QtWidgets.QVBoxLayout()
        search_params_additional.addStretch()
        search_params_additional.addLayout(age_param)
        search_params_additional.addLayout(duration_param)
        search_params_additional.addLayout(published_param)
        search_params_additional.addWidget(status_param)

        content_layout.addLayout(search_params_additional, 1, 2)

        self.content_area.setLayout(content_layout)

        collapsed_height = (self.sizeHint().height() - self.content_area.maximumHeight())
        content_height = content_layout.sizeHint().height()

        for index in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(index)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

    @QtCore.pyqtSlot()
    def on_toggle_button_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(QtCore.Qt.ArrowType.UpArrow if not checked else QtCore.Qt.ArrowType.DownArrow)
        self.toggle_animation.setDirection(
            QtCore.QAbstractAnimation.Direction.Forward
            if not checked
            else QtCore.QAbstractAnimation.Direction.Backward
        )
        self.toggle_animation.start()


class SearchParamList(QtWidgets.QWidget):
    def __init__(self, param_title, db_column, db_table):
        super(SearchParamList, self).__init__()

        title_label = QtWidgets.QLabel(param_title)
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        options_widget = SearchParamListOptions(db_column, db_table)

        group_vbox = QtWidgets.QVBoxLayout()
        group_vbox.addWidget(title_label)
        group_vbox.addWidget(options_widget)

        self.setLayout(group_vbox)


class SearchParamListOptions(QtWidgets.QListWidget):
    def __init__(self, db_column_from_parent, db_table_from_parent):
        super(SearchParamListOptions, self).__init__()

        self.setSortingEnabled(True)

        group_options = DatabaseHandler.get_distinct_values(db_column_from_parent, db_table_from_parent)
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


class SearchParamRanged(QtWidgets.QHBoxLayout):
    def __init__(self, range_name, input_width, input_length):
        super(SearchParamRanged, self).__init__()

        label = QtWidgets.QLabel(range_name)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        input_from = self.input_widget(input_width, input_length)
        dash_label = QtWidgets.QLabel('—')
        input_to = self.input_widget(input_width, input_length)

        self.addWidget(label)
        self.addWidget(input_from)
        self.addWidget(dash_label)
        self.addWidget(input_to)
        self.addStretch()

    @staticmethod
    def input_widget(input_width_from_init, input_length_from_init):
        input_line = QtWidgets.QLineEdit()
        input_line.setMaximumWidth(input_width_from_init)
        input_line.setMaxLength(input_length_from_init)

        return input_line


class SearchParamStatus(QtWidgets.QFrame):
    def __init__(self):
        super(SearchParamStatus, self).__init__()

        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        hbox = QtWidgets.QHBoxLayout()
        status_options_names = ['Online', 'Onsite', 'Archived']

        for name in status_options_names:
            status_option = QtWidgets.QCheckBox(name)
            hbox.addWidget(status_option)

        self.setLayout(hbox)


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

    app = QtWidgets.QApplication(sys.argv)

    filters = SearchFilters()

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(filters)

    selected_grid = QtWidgets.QGridLayout()
    selected_grid.addWidget(SelectedSearchOption('OOOO'))
    selected_grid.addWidget(SelectedSearchOption('1111'))

    main_window.resize(1280, 720)
    main_window.show()
    sys.exit(app.exec())
