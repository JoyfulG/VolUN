from PyQt6 import QtCore, QtWidgets

from selected_search_param import SelectedSearchParam


class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super(FlowLayout, self).__init__(parent)

        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontal_spacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        else:
            return self.smart_spacing(QtWidgets.QStyle.PixelMetric.PM_LayoutHorizontalSpacing)

    def vertical_spacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        else:
            return self.smart_spacing(QtWidgets.QStyle.PixelMetric.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(0)  # PyQt5 version. Haven't noticed any effect though

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.do_layout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def do_layout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineheight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontal_spacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.ControlType.PushButton,
                    QtWidgets.QSizePolicy.ControlType.PushButton, QtCore.Qt.Orientation.Horizontal)
            vspace = self.vertical_spacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.ControlType.PushButton,
                    QtWidgets.QSizePolicy.ControlType.PushButton, QtCore.Qt.Orientation.Vertical)
            next_x = x + item.sizeHint().width() + hspace
            if next_x - hspace > effective.right() and lineheight > 0:
                x = effective.x()
                y = y + lineheight + vspace
                next_x = x + item.sizeHint().width() + hspace
                lineheight = 0
            if not testonly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
            x = next_x
            lineheight = max(lineheight, item.sizeHint().height())

        return y + lineheight - rect.y() + bottom

    def smart_spacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()


if __name__ == '__main__':
    import sys


    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self, text, parent=None):
            super(MainWindow, self).__init__(parent)
            self.mainArea = QtWidgets.QScrollArea(self)
            self.mainArea.setWidgetResizable(True)
            widget = QtWidgets.QWidget(self.mainArea)
            widget.setMinimumWidth(50)
            layout = FlowLayout(widget)
            self.words = []
            for word in text.split():
                label = SelectedSearchParam(word)
                self.words.append(label)
                layout.addWidget(label)
            self.mainArea.setWidget(widget)
            self.setCentralWidget(self.mainArea)


    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow('Harry Potter is a series of fantasy literature')
    window.show()
    sys.exit(app.exec())
