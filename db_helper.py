# -*- coding: utf-8 -*-
"""
    Модуль содержащий реализацию работы с БД

    author: Шамхалов Р.М.
"""

import pymongo


def upsert_many(data: list):
    """
    Метод для множественной вставки информации по вакансиям.
    (специально сделано подключение каждое обрещаение,
    чтобы проходило больше времени между запросами к API HH)
    :param data: массив словарей с данными по вакансиям
    :return:
    """
    client = pymongo.MongoClient()
    db = client.vacancies
    collection = db.vacancy
    for vacancy in data:
        collection.save(vacancy)
