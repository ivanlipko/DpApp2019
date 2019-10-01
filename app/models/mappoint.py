#!/usr/bin/env python
# coding=utf-8
import datetime
import json

from app.database import DB

collection_mapPoints = 'map_points'
collection_routePoints = 'route_points'


class MapPoint(object):
    """
     [{"latitude": 55.7979071, "longitude": 49.1157559, "provider": "MTS RUS", "signalStrength": 2, "signalType": "4g",
       "time": 1569707330024}]

    """
    def __init__(self, provider, signalStrength, lat, long, signalType, time):
        self.provider = provider
        self.latitude = lat
        self.longitude = long
        self.signalStrength = signalStrength
        self.signalType = signalType
        self.time = time
        self.dbAddDate = datetime.datetime.utcnow()

    def insert(self):
        if not DB.find_one(collection_mapPoints, {'provider': self.provider,
                                                  'location': {
                                                      'type': "Point",
                                                      'coordinates': [self.latitude, self.longitude]},
                                                  'signalStrength': self.signalStrength,
                                                  'signalType': self.signalType,
                                                  'time': self.time,
                                                  'dbAddDate': self.dbAddDate}):
            DB.insert(collection=collection_mapPoints, data=self.json())

    def json(self):
        return {'provider': self.provider,
                  'location': {
                      'type': "Point",
                      'coordinates': [self.latitude, self.longitude]},
                  'signalStrength': self.signalStrength,
                  'signalType': self.signalType,
                  'time': self.time,
                  'dbAddDate': self.dbAddDate
                }


class MapRoute(object):
    def __init__(self, route_name, points):
        # self.route_name = route_name
        # self.points = points
        # self.created_date = datetime.datetime.utcnow()
        if not type(points) == list:
            print('points not dict')
        # self.data =
        self.route_name = route_name
        self.points = points
        # DB.route_points.createIndex({"location": "2dsphere"})

    def insert(self):
        DB.insert(collection=collection_routePoints, data=self.json())

    def json(self):
        # ress = json.dumps(self.data)
        return {'route_name': self.route_name,
                'points': {'type': 'LineString', 'coordinates': self.points}
                }
        # ress = {
        #     'route_name': self.route_name,
        #     'points': {type: 'LineString', 'coordinates': self.coordinates}
        #     # 'created_date': self.data.created_date
        # }
        # return self.data

# print(mp.json())

# mp = MapRoute(route_name='new_route', points=[[6, 7], [8, 9], [10, 11]])
