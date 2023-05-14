from PyQt6 import QtWidgets

from search_filters_widget import SearchFiltersWidget
from selected_search_param import SelectedSearchParam


class SearchWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SearchWidget, self).__init__()

        vbox = QtWidgets.QVBoxLayout()
        filters = SearchFiltersWidget()
        vbox.addWidget(filters)

        # temp_start
        # Should be SelectedSearchParamsWidget instead
        selected = QtWidgets.QHBoxLayout()
        selected.addWidget(SelectedSearchParam('OOOO'))
        selected.addWidget(SelectedSearchParam('1111'))
        vbox.addLayout(selected)
        # temp_finish

        vbox.addStretch()
        self.setLayout(vbox)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    filtersss = SearchWidget()

    window = QtWidgets.QWidget()
    vboxx = QtWidgets.QVBoxLayout(window)
    vboxx.addWidget(filtersss)

    window.resize(1280, 720)
    window.show()
    sys.exit(app.exec())
