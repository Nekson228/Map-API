import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from io import BytesIO
import requests
from PIL import Image


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


def search_func(coordinates, zoom):  # Функция поиска
    coordinates = ''.join(coordinates.split()).split(',')  # разбивка координат
    map_params = {
        "ll": ','.join([coordinates[1], coordinates[0]]),
        "z": int(zoom),
        "l": "map"
    }  # Формирование запроса

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params) # Отправка запроса

    return Image.open(BytesIO(response.content))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
