import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests

COORDINATES = '50.003193, 36.329676'
spn = [0.01, 0.01]


def search_func(coordinates):  # Функция поиска
    coordinates = ''.join(coordinates.split()).split(',')  # разбивка координат
    map_params = {
        "ll": ','.join([coordinates[1], coordinates[0]]),
        'spn': ','.join(map(str, spn)),
        "l": "map"
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
        self.search()

    def search(self):
        pixmap = QPixmap(search_func(COORDINATES))
        self.map_image.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if spn != [0.00015625, 0.00015625]:
                spn[0] /= 2
                spn[1] /= 2
                self.search()
        if event.key() == Qt.Key_PageDown:
            if spn != [81.92, 81.92]:
                spn[0] *= 2
                spn[1] *= 2
                self.search()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
