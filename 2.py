import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            zoom = self.zoom_slider.value()
            zoom += 1
            zoom = zoom if zoom < 20 else 20
            self.zoom_slider.setValue(zoom)
            self.search()
        if event.key() == Qt.Key_PageDown:
            zoom = self.zoom_slider.value()
            zoom -= 1
            zoom = zoom if zoom > 0 else 0
            self.zoom_slider.setValue(zoom)
            self.search()

    def search(self):
        coords = self.coords_input.text()
        if not coords:
            return
        zoom = self.zoom_slider.value()
        pixmap = QPixmap(search_func(coords, zoom))
        self.map_image.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())