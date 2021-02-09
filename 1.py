import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
import requests


def search_func(coordinates, zoom):  # Функция поиска
    coordinates = ''.join(coordinates.split()).split(',')  # разбивка координат
    map_params = {
        "ll": ','.join([coordinates[1], coordinates[0]]),
        "z": int(zoom),
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
        self.search_button.clicked.connect(self.search)

    def search(self):
        coords = self.coords_input.text()
        zoom = self.zoom_slider.value()
        print(coords, zoom)
        # вызов функции вани
        # вставка в лабел
        pixmap = QPixmap(search_func(coords, zoom))
        self.map_image.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
