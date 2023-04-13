from PyQt6 import QtWidgets, QtCore


class ShowPreviews(QtWidgets.QScrollArea):
    def __init__(self, previews):
        super(ShowPreviews, self).__init__()
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        widget = QtWidgets.QWidget()
        widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Preferred)
        vbox = QtWidgets.QVBoxLayout()

        for counter, preview in enumerate(previews):
            if counter % 2 != 0:
                preview.change_background_color('#b7dffd')
            vbox.addWidget(preview)

        vbox.addStretch(-1)
        widget.setLayout(vbox)
        self.setWidget(widget)
