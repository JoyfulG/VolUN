from PyQt6 import QtWidgets, QtCore

from database_handler import DatabaseHandler


class SearchParamList(QtWidgets.QWidget):
    def __init__(self, param_title, db_column, db_table):
        super(SearchParamList, self).__init__()

        title_label = QtWidgets.QLabel(param_title)
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        options_widget = self.SearchParamListOptions(db_column, db_table)

        group_vbox = QtWidgets.QVBoxLayout()
        group_vbox.addWidget(title_label)
        group_vbox.addWidget(options_widget)

        self.setLayout(group_vbox)

    class SearchParamListOptions(QtWidgets.QListWidget):
        def __init__(self, db_column_from_parent, db_table_from_parent):
            super(SearchParamList.SearchParamListOptions, self).__init__()

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


class SearchParamRanged(QtWidgets.QVBoxLayout):
    def __init__(self, range_name, input_width, input_length):
        super(SearchParamRanged, self).__init__()

        label = QtWidgets.QLabel(range_name)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        input_from = self.input_widget(input_width, input_length)
        dash_label = QtWidgets.QLabel('—')
        input_to = self.input_widget(input_width, input_length)
        input_hbox = QtWidgets.QHBoxLayout()
        input_hbox.addStretch()
        input_hbox.addWidget(input_from)
        input_hbox.addWidget(dash_label)
        input_hbox.addWidget(input_to)
        input_hbox.addStretch()

        self.addWidget(label)
        self.addLayout(input_hbox)

    @staticmethod
    def input_widget(input_width_from_init, input_length_from_init):
        input_line = QtWidgets.QLineEdit()
        input_line.setMaximumWidth(input_width_from_init)
        input_line.setMaxLength(input_length_from_init)

        return input_line


class SearchParamAssgnType(QtWidgets.QFrame):
    def __init__(self):
        super(SearchParamAssgnType, self).__init__()

        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        hbox = QtWidgets.QHBoxLayout()
        status_options_names = ['Online', 'Onsite', 'Archived']

        for name in status_options_names:
            status_option = QtWidgets.QCheckBox(name)
            hbox.addWidget(status_option)

        self.setLayout(hbox)
