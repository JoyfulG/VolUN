from PyQt6 import QtWidgets

from search.search_filters_widget import SearchFiltersWidget


class SearchWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SearchWidget, self).__init__()

        vbox = QtWidgets.QVBoxLayout()
        filters = SearchFiltersWidget()
        vbox.addWidget(filters)
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
