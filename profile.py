from PyQt6 import QtWidgets, QtGui, QtCore


class ProfilePicture(QtWidgets.QLabel):
    def __init__(self, image, target_size):
        super(ProfilePicture, self).__init__()
        source = QtGui.QPixmap(image)
        size = min(source.width(), source.height())

        target = QtGui.QPixmap(size, size)
        target.fill(QtCore.Qt.GlobalColor.transparent)

        painter = QtGui.QPainter(target)
        painter.setRenderHints(painter.RenderHint.Antialiasing)
        path = QtGui.QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)

        source_rect = QtCore.QRect(0, 0, size, size)
        source_rect.moveCenter(source.rect().center())
        painter.drawPixmap(target.rect(), source, source_rect)
        painter.end()

        self.setPixmap(target.scaled(target_size, target_size))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pic = ProfilePicture('test_pp.jpg', 150)
    pic.show()
    sys.exit(app.exec())
