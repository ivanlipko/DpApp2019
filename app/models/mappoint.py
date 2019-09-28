#!/usr/bin/env python
# coding=utf-8
import datetime

from app.database import DB

collection_mapPoints = 'map_points'


class mapPoint(object):
    """
        operator - название/тип оператора (строка)
        lat - координата latitude широта (число)
        long - координата longitude долгота (число)
        power - мощность сигнала (число)
        network_type - тип сигнала (2g,3g,4g)
        id1 - номер точки (число), не обязательный параметр

        _id - внутренний параметр БД, не изменяется, нигде не исопльзуется
    """

    def __init__(self, operator, power, lat, long, network_type, id1):
        self.operator = operator
        self.lat = lat
        self.long = long
        self.power = power
        self.network_type = network_type
        self.id = id1
        self.created_date = datetime.datetime.utcnow()

    def insert(self):
        if not DB.find_one(collection_mapPoints, {'operator': self.operator,
                                                  'lat': self.lat,
                                                  'long': self.long,
                                                  'power': self.power,
                                                  'network_type': self.network_type,
                                                  'id': self.id,
                                                  'created_date': self.created_date}):
            DB.insert(collection=collection_mapPoints, data=self.json())

    def json(self):
        return {
            'operator': self.operator,
            'lat': self.lat,
            'long': self.long,
            'power': self.power,
            'network_type': self.network_type,
            'id': self.id,
            'created_date': self.created_date
        }
