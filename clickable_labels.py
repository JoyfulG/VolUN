from PyQt6 import QtWidgets, QtCore


class QLabelClickable(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, func, *args, **kwargs):
        super(QLabelClickable, self).__init__(*args, **kwargs)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(func)

    def mousePressEvent(self, ev):
        self.clicked.emit()


class QLabelClickableUnderline(QLabelClickable):
    def __init__(self, *args, **kwargs):
        super(QLabelClickableUnderline, self).__init__(*args, **kwargs)

    def enterEvent(self, ev):
        self.underline_label(True)

    def leaveEvent(self, ev):
        self.underline_label(False)

    def underline_label(self, state):
        font = self.font()
        font.setUnderline(state)
        self.setFont(font)
