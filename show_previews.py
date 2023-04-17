from PyQt6 import QtWidgets, QtCore

from assignment_preview import AssignmentPreview


class ShowPreviews(QtWidgets.QScrollArea):
    def __init__(self, previews_data):
        super(ShowPreviews, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        widget = QtWidgets.QWidget()
        widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Preferred)
        vbox = QtWidgets.QVBoxLayout()

        previews = [AssignmentPreview(data) for data in previews_data]

        for counter, preview in enumerate(previews):
            if counter % 2 != 0:
                preview.change_background_color('#b7dffd')
            vbox.addWidget(preview)

        vbox.addStretch(-1)
        widget.setLayout(vbox)
        self.setWidget(widget)


if __name__ == '__main__':
    import sys
    from database_handler import DatabaseHandler
    app = QtWidgets.QApplication(sys.argv)
    data_test_previews = DatabaseHandler.get_previews_info()
    window = ShowPreviews(data_test_previews)
    window.show()
    sys.exit(app.exec())
