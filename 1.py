import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.search_button.clicked.connect(self.search)

    def search(self):
        coords = self.coords_input.text()
        zoom = self.zoom_slider.value()
        print(coords, zoom)
        # вызов функции вани
        # вставка в лабел


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
