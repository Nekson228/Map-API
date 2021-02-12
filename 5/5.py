import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests


def lonlat_size(lower, upper):
    lower, upper = list(map(float, lower.split())), list(map(float, upper.split()))
    return [abs(lower[0] - upper[0]), abs(lower[1] - upper[1])]


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.current_type = 'map'
        self.spn = [0.01, 0.01]
        self.ll = None
        self.current_address = None
        self.original_point = None

        self.type_box.currentIndexChanged.connect(self.change_type)
        self.search_button.clicked.connect(self.search)

    def change_type(self):
        self.current_type = self.type_box.currentText().split(' - ')[1]
        if self.adress_input.text():
            self.search()

    def search(self):
        if self.adress_input.text():
            if self.current_address != self.adress_input.text() or not self.ll:
                parameters = {
                    'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                    'geocode': self.adress_input.text(),
                    'format': 'json'
                }
                geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"

                response = requests.get(geocoder_request, params=parameters)
                json_response = response.json()

                try:
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                except IndexError:
                    self.statusBar().showMessage('Ничего не найдено')
                    return
                toponym_coodrinates = toponym["Point"]["pos"]
                self.ll = list(map(float, toponym_coodrinates.split()))
                self.original_point = self.ll.copy()
                self.current_address = self.adress_input.text()

                toponym_bbox = toponym['boundedBy']['Envelope']
                self.spn = lonlat_size(toponym_bbox['lowerCorner'], toponym_bbox['upperCorner'])
            pixmap = QPixmap(self.search_func())
            self.map_image.setPixmap(pixmap)

    def search_func(self):  # Функция поиска
        map_params = {
            "ll": ','.join([str(self.ll[0]), str(self.ll[1])]),
            'pt': ','.join([str(self.original_point[0]), str(self.original_point[1])]),
            'spn': ','.join(map(str, self.spn)),
            "l": self.current_type,
        }  # Формирование запроса

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)  # Отправка запроса
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        return map_file

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.spn[0] > 0.0002 and self.spn[1] > 0.0002:
                self.spn[0] /= 2
                self.spn[1] /= 2
                self.search()
        if event.key() == Qt.Key_PageDown:
            if self.spn[0] < 62.5 and self.spn[1] < 62.5:
                self.spn[0] *= 2
                self.spn[1] *= 2
                self.search()
        if event.key() == Qt.Key_Up:
            self.ll[1] += self.spn[1]
            self.search()
        if event.key() == Qt.Key_Down:
            self.ll[1] -= self.spn[1]
            self.search()
        if event.key() == Qt.Key_Right:
            self.ll[0] += self.spn[0]
            self.search()
        if event.key() == Qt.Key_Left:
            self.ll[0] -= self.spn[0]
            self.search()

    def closeEvent(self, event):
        os.remove('map.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
