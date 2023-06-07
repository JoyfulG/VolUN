from PyQt6 import QtWidgets, QtCore

from search.flow_layout import FlowLayout
from search.selected_search_param import SelectedSearchParamCheckbox, SelectedSearchParamRanged


class SelectedSearchParamsWidget(QtWidgets.QScrollArea):
    def __init__(self):
        super(SelectedSearchParamsWidget, self).__init__()

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMaximumHeight(40)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        widget = QtWidgets.QWidget()
        self.layout = FlowLayout(widget)
        self.setWidget(widget)

    def add_checkbox_item(self, item):
        bubble = SelectedSearchParamCheckbox(item)
        self.layout.addWidget(bubble)

    def add_ranged_item(self, item):
        bubble = SelectedSearchParamRanged(item)
        self.layout.addWidget(bubble)

    def remove_item(self, item):
        index = self.layout.count()
        while index:
            layout_item = self.layout.itemAt(index - 1)
            if item == layout_item.widget().item:
                self.layout.removeWidget(layout_item.widget())
                break
            index -= 1
