# -*- coding: utf-8 -*-
"""
    Модуль содержащий реализацию работы с API hh.ru.

    author: Шамхалов Р.М.
"""

import requests
import json
import filter
from base import WorkPool


class Hh(WorkPool):

    token = ''

    @staticmethod
    def check_token() -> bool:
        """
        Метод для проверки валидности токена приложения
        :return: True если токен валидный, иначе False
        """
        url = 'https://api.hh.ru/me'
        res = requests.get(url=url,
                           headers={'Authorization': f'Bearer {Hh.token}'})

        print(res.json())
        for key, value in res.json().items():
            if value:
                return True
        return False

    @staticmethod
    def get_vacancies(query_filter: str):
        """
        Метод для получения вакансии по переданному фильтру
        :param query_filter: фильтр для получения вакансий
        :return:
        """
        url = f'https://api.hh.ru/vacancies?{query_filter}'

        res = requests.get(url=url,
                           headers={'Authorization': f'Bearer {Hh.token}'})

        print(res.text)
        ans = res.json().get("items")
        for i in ans:
            print(i.get("alternate_url"))
        # print(json.dumps(ans))

    @staticmethod
    def start_pool():
        """
        Метод стартует сбор данных из hh.
        (Соберет все необходимые фильтры, заберет 2000 с каждого фильтра и положит в БД)
        :return:
        """
        print("задание начал")


# print(Hh.check_token())
# Hh.get_vacancies('salary=20000&per_page=2&page=5&only_with_salary=true')

