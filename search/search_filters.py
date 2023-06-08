from PyQt6 import QtWidgets, QtCore, QtGui

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
            self.itemChanged.connect(self.on_item_changed)

        def toggle_item(self, item):
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            else:
                item.setCheckState(QtCore.Qt.CheckState.Checked)

        def on_item_changed(self, item):
            selected_options = self.parent().parent().parent().layout().itemAt(2).widget()
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                selected_options.add_checkbox_item(item)
            else:
                selected_options.remove_item(item)


class SearchParamRanged(QtWidgets.QVBoxLayout):
    def __init__(self, range_name, input_width, input_length):
        super(SearchParamRanged, self).__init__()

        label = QtWidgets.QLabel(range_name)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.input_from = self.input_widget(input_width, input_length)
        dash_label = QtWidgets.QLabel('—')
        self.input_to = self.input_widget(input_width, input_length)
        input_hbox = QtWidgets.QHBoxLayout()
        input_hbox.addStretch()
        input_hbox.addWidget(self.input_from)
        input_hbox.addWidget(dash_label)
        input_hbox.addWidget(self.input_to)
        input_hbox.addStretch()

        self.addWidget(label)
        self.addLayout(input_hbox)

    def input_widget(self, input_width_from_init, input_length_from_init):
        input_line = QtWidgets.QLineEdit()
        regexp = QtCore.QRegularExpression('(^[0-9]+$|^$)')
        input_line.setValidator(QtGui.QRegularExpressionValidator(regexp))
        input_line.setMaximumWidth(input_width_from_init)
        input_line.setMaxLength(input_length_from_init)
        input_line.textChanged.connect(self.on_text_changed)

        return input_line

    def on_text_changed(self):
        selected_options = self.parent().parent().parent().parent().parent().layout().itemAt(2).widget()
        index = selected_options.layout.count()
        while index:
            layout_item = selected_options.layout.itemAt(index - 1)
            if self == layout_item.widget().item:
                if self.input_from.text() == '' and self.input_to.text() == '':
                    selected_options.remove_item(self)
                    break
                selected_options.change_ranged_item(self, index - 1)
                break
            index -= 1
        else:
            selected_options.add_ranged_item(self)


class SearchParamAssgnType(QtWidgets.QFrame):
    def __init__(self):
        super(SearchParamAssgnType, self).__init__()

        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)

        hbox = QtWidgets.QHBoxLayout()
        status_options_names = ['Online', 'Onsite', 'Archived']

        for name in status_options_names:
            status_option = QtWidgets.QCheckBox(name)
            status_option.stateChanged.connect(self.on_option_state_changed)
            hbox.addWidget(status_option)

        self.setLayout(hbox)

    def on_option_state_changed(self):
        selected_options = self.parent().parent().layout().itemAt(2).widget()
        checkbox = self.sender()
        if checkbox.checkState() == QtCore.Qt.CheckState.Checked:
            selected_options.add_checkbox_item(checkbox)
        else:
            selected_options.remove_item(checkbox)
