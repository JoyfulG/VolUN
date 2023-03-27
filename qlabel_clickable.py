import sys

from PyQt6 import QtWidgets, QtCore


class QLabelClickable(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, func, *args, **kwargs):
        super(QLabelClickable, self).__init__(*args, **kwargs)
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(func)

    def mousePressEvent(self, ev):
        self.clicked.emit()


if __name__ == '__main__':
    def test():
        print('Label clicked')

    app = QtWidgets.QApplication(sys.argv)
    contents = QLabelClickable(test, 'Text')
    contents.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    vbox = QtWidgets.QVBoxLayout()
    vbox.addWidget(contents)
    vbox.addStretch()
    window = QtWidgets.QWidget()
    window.setLayout(vbox)
    window.show()
    sys.exit(app.exec())
