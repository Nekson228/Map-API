import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests

COORDINATES = '50.003193, 36.329676'


def search_func(ll, spn, map_type):  # Функция поиска
    map_params = {
        "ll": ','.join([str(ll[1]), str(ll[0])]),
        'spn': ','.join(map(str, spn)),
        "l": map_type
    }  # Формирование запроса

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)  # Отправка запроса
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.current_type = 'map'
        self.spn = [0.01, 0.01]
        self.ll = [float(i) for i in ''.join(COORDINATES.split()).split(',')]

        self.type_box.currentIndexChanged.connect(self.change_type)
        self.search()

    def change_type(self):
        self.current_type = self.type_box.currentText().split(', ')[1]
        self.search()

    def search(self):
        pixmap = QPixmap(search_func(self.ll, self.spn, self.current_type))
        self.map_image.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn[0] += 0.005
            self.spn[1] += 0.005
            self.search()
        if event.key() == Qt.Key_PageDown:
            self.spn[0] -= 0.005
            self.spn[1] -= 0.005
            self.search()
        if event.key() == Qt.Key_Up:
            self.ll[0] += self.spn[0]
            self.search()
        if event.key() == Qt.Key_Down:
            self.ll[0] -= self.spn[0]
            self.search()
        if event.key() == Qt.Key_Right:
            self.ll[1] += self.spn[1]
            self.search()
        if event.key() == Qt.Key_Left:
            self.ll[1] -= self.spn[1]
            self.search()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
