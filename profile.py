from PyQt6 import QtWidgets, QtGui, QtCore


class ProfilePicture(QtWidgets.QLabel):
    def __init__(self, image, target_size):
        super(ProfilePicture, self).__init__()
        source = QtGui.QPixmap(image)
        size = min(source.width(), source.height())
        source_rect = QtCore.QRect(0, 0, size, size)
        source_rect.moveCenter(source.rect().center())

        target = QtGui.QPixmap(target_size, target_size)
        target.fill(QtCore.Qt.GlobalColor.transparent)

        path = QtGui.QPainterPath()
        path.addEllipse(0, 0, target_size, target_size)

        painter = QtGui.QPainter(target)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setClipPath(path)
        painter.drawPixmap(target.rect(), source, source_rect)
        painter.end()

        self.setPixmap(target)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pic = ProfilePicture('test_pp.jpg', 150)
    pic.show()
    sys.exit(app.exec())
