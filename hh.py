# -*- coding: utf-8 -*-
"""
    Модуль содержащий реализацию работы с API hh.ru.

    author: Шамхалов Р.М.
"""

import json
import time
import requests
import itertools
from datetime import timedelta, datetime

import filter
import db_helper
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

        return res.json()

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
    def parse_vacancies(vacancies: dict, employment: str) -> list:
        """
        Методя для парсинга сырых данных от hh
        :param vacancies: массив с данными по вакансиям
        :param employment: тип занятости, передается тк есть у нас в фильтре
        :return: массив словарей по формату для записи в бд
        """
        result = []

        for vacancy in vacancies.get("items"):
            result.append(
                {"id": vacancy.get("id"),
                 "name": vacancy.get("name"),
                 "published_date": vacancy.get("published_at"),
                 "created_date": vacancy.get("created_at"),
                 "employment": employment,
                 "schedule": vacancy.get("schedule").get("name"),
                 "city": vacancy.get("area").get("name"),
                 "salary": vacancy.get("salary"),
                 "archived": vacancy.get("archived")})

        return result

    @staticmethod
    def start_pool():
        """
        Метод стартует сбор данных из hh.
        (Соберет все необходимые фильтры, заберет 2000 с каждого фильтра и положит в БД)
        :return:
        """
        date_start = datetime.strptime(filter.DATE_FROM, "%Y-%m-%d").date()
        date_end = datetime.strptime(filter.DATE_TO, "%Y-%m-%d").date()
        delta = timedelta(days=2)

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
                                      "only_with_salary": True,
                                      "describe_arguments": True}
                    # Получаем информацию по заданному фильтру
                    vacancies_info = Hh.get_vacancies(current_filter)
                    # Если вакансий не вернулось, то переходим к следующему фильтру
                    if not vacancies_info.get("items"):
                        time.sleep(1)
                        break
                    # Дальше надо запарсить данные под формат вставки в БД
                    parse_vacancies_info = Hh.parse_vacancies(vacancies_info, empl)
                    # Запись в базу
                    db_helper.upsert_many(parse_vacancies_info)
            date_start = current_date_end


# print(Hh.get_dict_info())
# print(Hh.check_token())
# filter = {"salary": 20000, "per_page": 10, "page": 1, "only_with_salary": True}
Hh.start_pool()
# Hh.get_vacancies('salary=20000&per_page=100&page=19&only_with_salary=true')

