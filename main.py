import sys

from PyQt6 import QtWidgets, QtGui, QtCore


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('VolUN')
        self.setWindowIcon(QtGui.QIcon('volun_icon.png'))
        self.resize(1200, 700)
        self.setMinimumSize(500, 350)

        self.userpic = profile_picture('test_pp.jpg')
        self.username_label = profile_name('TestUsername')
        self.home_button = home_btn()

        self.userpic_label = QtWidgets.QLabel()
        self.userpic_label.setPixmap(self.userpic.scaled(150, 150))
        self.userpic_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.docked_vbox = QtWidgets.QVBoxLayout()
        self.docked_vbox.addWidget(self.userpic_label)
        self.docked_vbox.addWidget(self.username_label)
        self.docked_vbox.addWidget(self.home_button)
        self.docked_vbox.addStretch()

        self.docked_label = QtWidgets.QLabel()
        self.docked_label.setLayout(self.docked_vbox)

        self.docked_menu = QtWidgets.QDockWidget()
        self.docked_menu.setFixedWidth(330)
        self.docked_menu.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.docked_menu.setTitleBarWidget(QtWidgets.QWidget())  # Getting rid of the docked_menu title bar.
        self.docked_menu.setWidget(self.docked_label)

        self.setCentralWidget(QtWidgets.QTextEdit())
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.docked_menu)

        self.show()


def profile_picture(image):
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

    return target


def profile_name(name):
    name_label = QtWidgets.QLabel()
    name_label.setText(f'<b>{name}</b>')
    name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    name_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
    name_label.setFont(QtGui.QFont('Arial', 16))

    return name_label


def home_btn():
    btn = QtWidgets.QPushButton('Home')

    return btn



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
