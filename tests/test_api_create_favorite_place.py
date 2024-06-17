import unittest
from http import HTTPStatus

import requests

from constants import URL


class TestAPICase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.correct_data = dict(
            title="Место123",
            lat=55.028254,
            lon=82.918501
        )
        cls.correct_answer = dict(
            title="Место123",
            lat=55.028254,
            lon=82.918501,
            color=None,
        )
        cls.empty_title = dict(
            lat=55.028254,
            lon=82.918501
        )
        cls.empty_lat = dict(
            title="Место1",
            lon=82.918501
        )
        cls.empty_lon = dict(
            title="Место1",
            lat=55.028254,
        )
        cls.incorrect_min_len_title = dict(
            title="",
            lat=55.028254,
            lon=82.918501
        )
        cls.incorrect_max_len_title = dict(
            title="".join(str(i) for i in range(1500)),
            lat=55.028254,
            lon=82.918501
        )
        cls.incorrect_type_lat = dict(
            title="Место1",
            lat="где-то тут",
            lon=82.918501
        )
        cls.incorrect_type_lon = dict(
            title="Место1",
            lat=55.028254,
            lon="где то там"
        )

        cls.url = URL + "/v1/favorites"

    def setUp(self):
        self.session = requests.Session()
        self.session.post(URL + "/v1/auth/tokens")
        self.cookies = self.session.cookies.get_dict()

    def test_not_auth(self):
        """Проверка работы без авторизации."""

        response = self.session.post(
            self.url, data=self.correct_data
        )
        self.assertEqual(
            response.status_code, HTTPStatus.UNAUTHORIZED,
            "Необходима авторизация."
        )

    def test_correct(self):
        """Проверка позитивного примера."""

        response = self.session.post(
            self.url, data=self.correct_data, cookies=self.cookies
        )
        self.assertEqual(
            response.status_code, HTTPStatus.OK,
            "При успешном создании должен возвращаться код 200"
        )
        data = dict(response.json())
        for key, value in self.correct_answer.items():
            self.assertIn(
                key, data.keys(), "В ответе отсутствует ключ {}".format(key)
            )
            self.assertIn(
                value, data.values(),
                "В ответе отсутствует значение {}".format(value)
            )
        self.assertIn(
            "created_at", data.keys(), "В ответе отсутствует ключ created_at"
        )

    def test_get_request(self):
        """Проверка GET запроса."""

        response = self.session.get(
            self.url, data=self.correct_data, cookies=self.cookies
        )
        self.assertEqual(
            response.status_code, HTTPStatus.METHOD_NOT_ALLOWED,
            "GET запрос не разрешен. Только POST."
        )

    def test_empty_title(self):
        """Проверка запросы без title"""
        response = self.session.post(
            self.url, data=self.empty_title, cookies=self.cookies
        )
        self.assertEqual(
            response.status_code, HTTPStatus.BAD_REQUEST,
            "Параметр 'title' является обязательным. StatusCode должен быть 400"
        )
        self.assertEqual(
            dict(response.json())["error"]["message"],
            "Параметр 'title' является обязательным"
        )

    def test_empty_lat(self):
        """Проверка запросы без lat"""

        response = self.session.post(
            self.url, data=self.empty_lat, cookies=self.cookies
        )
        self.assertEqual(
            response.status_code, HTTPStatus.BAD_REQUEST,
            "Параметр 'lat' является обязательным. StatusCode должен быть 400"
        )
        self.assertEqual(
            dict(response.json())["error"]["message"],
            "Параметр 'lat' является обязательным"
        )

    def test_empty_lon(self):
        """Проверка запросы без lon"""

        response = self.session.post(
            self.url, data=self.empty_lon, cookies=self.cookies
        )
        self.assertEqual(
            response.status_code, HTTPStatus.BAD_REQUEST,
            "Параметр 'lon' является обязательным. StatusCode должен быть 400"
        )
        self.assertEqual(
            dict(response.json())["error"]["message"],
            "Параметр 'lon' является обязательным"
        )

    def test_incorrect_min_len_title(self):
        """Проверка минимальной длины заголовка."""

        response = self.session.post(
            self.url, data=self.incorrect_min_len_title, cookies=self.cookies
        )
        self.assertEqual(
            response.status_code, HTTPStatus.BAD_REQUEST,
            "Длина title должна быть больше 1"
        )

    def test_incorrect_max_len_title(self):
        """Проверка максимальной длины заголовка."""

        response = self.session.post(
            self.url, data=self.incorrect_max_len_title, cookies=self.cookies
        )
        self.assertEqual(
            response.status_code, HTTPStatus.BAD_REQUEST,
            "Длина title должна быть меньше 999"
        )

    def test_incorrect_type_lat(self):
        """Проверка типа данных для lat"""

        response = self.session.post(
            self.url, data=self.incorrect_type_lat, cookies=self.cookies
        )
        self.assertEqual(
            response.status_code, HTTPStatus.BAD_REQUEST,
            "Параметр 'lat' должен быть числом"
        )
        self.assertEqual(
            dict(response.json())["error"]["message"],
            "Параметр 'lat' должен быть числом"
        )

    def test_incorrect_type_lon(self):
        """Проверка типа данных для lon"""

        response = self.session.post(
            self.url, data=self.incorrect_type_lon, cookies=self.cookies
        )
        self.assertEqual(
            response.status_code, HTTPStatus.BAD_REQUEST,
            "Параметр 'lon' должен быть числом"
        )
        self.assertEqual(
            dict(response.json())["error"]["message"],
            "Параметр 'lon' должен быть числом"
        )

    def test_correct_color(self):
        colors = ["BLUE", "GREEN", "RED", "YELLOW"]
        input_data = self.correct_data
        output_data = []
        for color in colors:
            input_data["color"] = color
            response = self.session.post(
                self.url, data=input_data, cookies=self.cookies
            )
            output_data.append(response.json()["color"])
            self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(colors, output_data)

    def test_incorrect_color(self):
        colors = ["redddd"]
        input_data = self.correct_data
        for color in colors:
            input_data["color"] = color.upper()
            response = self.session.post(
                self.url, data=input_data, cookies=self.cookies
            )
            self.assertEqual(
                response.status_code,
                HTTPStatus.BAD_REQUEST,
                "Цвет должен быть только BLUE, GREEN, RED, YELLOW"
            )


if __name__ == '__main__':
    unittest.main()
