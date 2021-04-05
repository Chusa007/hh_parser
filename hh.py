# -*- coding: utf-8 -*-
"""
    Модуль содержащий реализацию работы с API hh.ru.

    author: Шамхалов Р.М.
"""

import requests
import json
import itertools
from datetime import timedelta, date, datetime
import filter
from base import WorkPool


class Hh(WorkPool):

    # Токен приложения hh
    token = ''
    # Максимальная страница вакансий
    max_page = 19

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
    def get_vacancies(query_filter: dict):
        """
        Метод для получения вакансии по переданному фильтру
        :param query_filter: фильтр для получения вакансий
        :return:
        """
        url = f'https://api.hh.ru/vacancies'

        res = requests.get(url=url,
                           params=query_filter,
                           headers={'Authorization': f'Bearer {Hh.token}'})

        print(res.text)
        print(res.url)
        ans = res.json().get("items")
        for i in ans:
            print(i.get("alternate_url"))
        # print(json.dumps(ans))

    @staticmethod
    def get_dict_info():
        """
        Метод для получения актуальной инфомарции по id фильтров
        :return:
        """
        url = f'https://api.hh.ru/dictionaries'

        res = requests.get(url=url,
                           headers={'Authorization': f'Bearer {Hh.token}'})

        print(res.json().get("employment"))

    @staticmethod
    def start_pool():
        """
        Метод стартует сбор данных из hh.
        (Соберет все необходимые фильтры, заберет 2000 с каждого фильтра и положит в БД)
        :return:
        """
        date_start = datetime.strptime(filter.DATE_FROM, "%Y-%m-%d").date()
        date_end = datetime.strptime(filter.DATE_TO, "%Y-%m-%d").date()
        delta = timedelta(days=3)

        # Основной цикл по дате
        while date_start <= date_end:
            current_date_end = date_start + delta
            # Собираем все возможные зарплатные сетки + типы занятости + субъекты
            for sal, area, empl in itertools.product(filter.SALARY, filter.AREA, filter.EMPLOYMENT):
                # Пагинация
                for page_number in range(0, Hh.max_page):
                    current_filter = {"salary": sal,
                                      "employment": empl,
                                      "area": area,
                                      "date_from": date_start.strftime("%Y-%m-%d"),
                                      "date_to": current_date_end.strftime("%Y-%m-%d"),
                                      "per_page": filter.PER_PAGE,
                                      "page": page_number,
                                      "only_with_salary": True}
                    # Получаем информацию по заданному фильтру
                    # vacancies_info = Hh.get_vacancies(current_filter)
                    # Дальше надо запарсить данные под формат вставки в БД
                    # Запись в базу
            date_start = current_date_end
        print("задание начал")


# print(Hh.get_dict_info())
# print(Hh.check_token())
# filter = {"salary": 20000, "per_page": 10, "page": 1, "only_with_salary": True}
# Hh.get_vacancies(filter)
# Hh.get_vacancies('salary=20000&per_page=100&page=19&only_with_salary=true')
