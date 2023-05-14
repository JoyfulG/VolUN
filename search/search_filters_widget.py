from PyQt6 import QtWidgets, QtCore

from search_filters import SearchParamList, SearchParamRanged, SearchParamAssgnType
from search_buttons import StartSearchButton, ClearAllButton


class SearchFiltersWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SearchFiltersWidget, self).__init__()

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
            ('Languages', 'lang', 'languages', 1, 0),
            ('Volunteer category', 'vol_category', 'assignments', 1, 1),
            ('Level of education', 'ed_lvl', 'assignments', 1, 2)
        ]

        for title, db_column, db_table, pos_row, pos_column in search_param_lists:
            search_param_list = SearchParamList(title, db_column, db_table)
            content_layout.addWidget(search_param_list, pos_row, pos_column)

        status_param = SearchParamAssgnType()
        age_param = SearchParamRanged('Age:', 25, 2)
        duration_param = SearchParamRanged('Duration:', 35, 4)

        age_and_duration_hbox = QtWidgets.QHBoxLayout()
        age_and_duration_hbox.addLayout(age_param)
        age_and_duration_hbox.addLayout(duration_param)

        search_params_additional = QtWidgets.QVBoxLayout()
        search_params_additional.addSpacing(31)
        search_params_additional.addWidget(status_param)
        search_params_additional.addSpacing(20)
        search_params_additional.addLayout(age_and_duration_hbox)
        search_params_additional.addSpacing(20)
        search_params_additional.addStretch()

        search_button = StartSearchButton()
        clear_button = ClearAllButton()
        buttons_vbox = QtWidgets.QVBoxLayout()
        buttons_vbox.addStretch()
        buttons_vbox.addWidget(clear_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        buttons_vbox.addWidget(search_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        buttons_vbox.addSpacing(8)
        content_layout.addLayout(buttons_vbox, 1, 3)

        content_layout.addLayout(search_params_additional, 0, 3)

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
