# -*- coding: utf-8 -*-

# Copyright 2019 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from flask import render_template, request, abort

from app.main import bp  # noqa
from app.models.mappoint import MapPoint, MapRoute, collection_mapPoints, collection_routePoints
from app.database import DB
from flask import jsonify


def del_obj_id(point):
    # task['_id'] = 0
    point['_id'] = str(point['_id'])
    # point['_id'] = 0
    return point


@bp.route('/')
def index():
    """Main page route."""
    return render_template('index.html')


'''
добавляем новую точку, поле operator - обязательное
curl -i -H "Content-Type: application/json" -X POST -d '{"operator":"mts", "lat":"44.53", "long":"39.56", "power":"-45.0", "network_type":"3g", "_id":"1"}' http://localhost:8080/add_point
curl -i -H "Content-Type: application/json" -X POST -d '{"operator":"tele2", "lat":"42.5876453", "long":"39.234556", "power":"-35.0", "network_type":"4g", "_id":"1"}' http://localhost:8080/add_point
curl -i -H "Content-Type: application/json" -X POST -d '{"operator":"megafon", "lat":"41.34553", "long":"33.45956", "power":"-55.0", "network_type":"3g", "_id":"1"}' http://localhost:8080/add_point
curl -i -H "Content-Type: application/json" -X POST -d '{"operator":"megafon", "lat":"44.34534553", "long":"32.12356", "power":"-25.0", "network_type":"2g", "_id":"1"}' http://localhost:8080/add_point

'''
@bp.route('/add_point', methods=['POST'])
def add_point():
    """Adds point to the database."""
    if not request.json or not 'operator' in request.json:
        abort(400)

    new_point = MapPoint(
        provider=request.json.get('provider', ''),
        lat=float(request.json.get('latitude', '')),
        long=float(request.json.get('longitude', '')),
        signalStrength=request.json.get('signalStrength', ''),
        signalType=request.json.get('signalType', ''),
        time=request.json.get('time', '')
    )
    new_point.insert()
    return jsonify(new_point.json()), 201

'''

add several points

curl -i -H "Content-Type: application/json" -X POST -d '[{"operator":"beeline", "lat":55.789190, "long":49.099508, "power":4, "network_type":"3g", "_id":1},{"operator":"beeline", "lat":55.789297, "long":49.099537, "power":1, "network_type":"3g", "_id":1},{"operator":"beeline", "lat":55.788837, "long":49.099434, "power":4, "network_type":"3g", "_id":1},{"operator":"beeline", "lat":55.788761, "long":49.099468, "power":1, "network_type":"3g", "_id":1}]' http://192.168.1.105:8080/add_points
curl -i -H "Content-Type: application/json" -X POST -d '[{"operator":"beeline", "lat":55.789190, "long":49.099508, "power":4, "network_type":"3g"},{"operator":"beeline", "lat":55.789297, "long":49.099537, "power":1, "network_type":"3g"},{"operator":"beeline", "lat":55.788837, "long":49.099434, "power":4, "network_type":"3g"},{"operator":"beeline", "lat":55.788761, "long":49.099468, "power":1, "network_type":"3g"}]' http://192.168.1.105:8080/add_points
curl -i -H "Content-Type: application/json" -X POST -d '[{"operator":"beeline", "lat":55.789190, "long":49.099508, "power":4, "network_type":"3g"},{"operator":"beeline", "lat":55.789297, "long":49.099537, "power":1, "network_type":"3g"},{"operator":"beeline", "lat":55.788837, "long":49.099434, "power":4, "network_type":"3g"},{"operator":"beeline", "lat":55.788761, "long":49.099468, "power":1, "network_type":"3g"}]' http://0.0.0.0:8080/add_points

curl -i -H "Content-Type: application/json" -X POST -d '[{"provider":"beeline1", "latitude":55.789190, "longitude":49.099508, "signalStrength":4, "signalType":"3g"},{"provider":"beeline2", "latitude":55.689190, "longitude":49.199508, "signalStrength":3, "signalType":"4g"},{"provider":"beeline3", "latitude":55.889190, "longitude":49.299508, "signalStrength":2, "signalType":"2g"},{"provider":"beeline", "latitude":55.989190, "longitude":49.399508, "signalStrength":0, "signalType":"5g"}]' http://0.0.0.0:8080/add_points

 [{"latitude": 55.7979071, "longitude": 49.1157559, "provider": "MTS RUS", "signalStrength": 2, "signalType": "4g",
       "time": 1569707330024}]

'''

@bp.route('/add_points', methods=['POST'])
def add_points():
    """Adds point to the database."""
    if not request.json: #or not 'points' in request.json:
        abort(400)

    print(type(request.json), request.json)
    for item in request.json:
        new_point = MapPoint(
            provider=item.get('provider', ''),
            lat=float( item.get('latitude', '')),
            long=float(item.get('longitude', '')),
            signalStrength=item.get('signalStrength', ''),
            signalType=item.get('signalType', ''),
            time=item.get('time', '')
        )
        new_point.insert()

    return jsonify({'received':len(request.json)}), 201


"""
get ALL collection_mapPoints of elements

получить список всех точек
curl -i http://localhost:8080/showall

"""
@bp.route('/showall')
def showall():
    # jobs = list(DB.jobs().find())  #оба варианта эквивалентны
    # points = list(DB.find("jobs"))
    # return render_template('jobs.html', jobs=points)
    points = [doc for doc in DB.find(collection_mapPoints)]
    points = list(map(del_obj_id, points))

    return jsonify(points), 200


'''

берём все точки, где оператор мегафон (в базе есть: mts, megafon, tele2)
curl -i -H "Content-Type: application/json" -X GET -d '{ "query": {"operator":"megafon"} }' http://localhost:8080/show

curl -i -H "Content-Type: application/json" -X GET -d '{ "query": {"operator":"mts"} }' http://localhost:8080/show

берём все точки, где тип сети 4g
curl -i -H "Content-Type: application/json" -X GET -d '{ "query": {"network_type":"4g"} }' http://localhost:8080/show

берём все точки, где тип сети 4g или 2g
curl -i -H "Content-Type: application/json" -X GET -d '{"query": {"network_type":{"$in":["4g","2g"]}} }' http://localhost:8080/show

берём все точки, где мощность сигнала больше
curl -i -H "Content-Type: application/json" -X GET -d '{"query": {"power":{"$lt":40}} }' http://localhost:8080/show

'''
@bp.route('/show', methods=['GET'])
def show_point():
    print(request.json)
    if not request.json or not 'query' in request.json:
        abort(400)
    query = request.json.get('query', '')
    points = [doc for doc in DB.find(collection_mapPoints, query=query)]
    points = list(map(del_obj_id, points))
    return jsonify(points), 200

'''
curl -i -H "Content-Type: application/json" -X POST -d '{"route_name":"new_route", "points":[[1, 2], [3, 4], [5, 6]]}' http://localhost:8080/add_route
'''
@bp.route('/add_route', methods=['POST'])
def add_route():
    if not request.json or not 'route_name' in request.json:
        abort(400)

    mp = MapRoute(route_name=request.json.get('route_name', ''),
                  points=request.json.get('points', ''))
    mp.insert()
    return jsonify(mp.json()), 201


@bp.route('/show_route_quality/', methods=['GET'])
def show_route():
    # print(request.json)
    # query = request.json.get('query', '')

    # get all routes
    all_routes = [doc for doc in DB.find(collection_routePoints)]

    # get one route
    route = DB.find_one(collection_routePoints, query={"route_name":"new_route"})

    places = []
    indx = -1
    route_points = list(route.get('points').get('coordinates'))
    for point in route_points:
        indx += 1
        # get nearest
        # qqq = {"location": {"$nearSphere": {"$geometry": {"type": "Point", "coordinates": point}, "$maxDistance": 15}}}
        query = {"location": {"$near": {"$geometry": {"type": "Point", "coordinates": point}, "$maxDistance": 1000}}}
        # points = DB.find(collection_mapPoints, query=qqq)
        points = [doc for doc in DB.find(collection_mapPoints, query=query)]
        points = list(map(del_obj_id, points))

        mean_strength = 0
        signalTypes = []

        if len(points) < 1:
            # print('len is zero')
            place = {'indx': indx, 'signalStrength': 0, 'signalType': [], 'location':point}
            places.append(place)
            continue

        for p in points:
            # print(p)
            mean_strength += p.get('signalStrength')
            signalTypes.append( p.get('signalType') )
        mean_strength = mean_strength/len(points)
        signalTypes = list(set(signalTypes))
        place = {'indx':indx, 'signalStrength':mean_strength, 'signalType':signalTypes, 'location':point}
        places.append(place)

    return jsonify(places), 200


@bp.errorhandler(404)
@bp.app_errorhandler(404)
def http_404_handler(error):
    return jsonify({'error': 'not found'}), 404


@bp.errorhandler(400)
@bp.app_errorhandler(400)
def http_400_handler(error):
    return jsonify({'error': 'data is missed'}), 400


@bp.errorhandler(500)
@bp.app_errorhandler(500)
def http_500_handler(error):
    return "<p>HTTP 500 Error Encountered</p>", 500


'''
@bp.route('/add_job')
def add_job():
    """Adds job4 to the database."""
    new_job = Job(name='job4')
    new_job.insert()
    return ('', 204)


"""get collection of elements"""
@bp.route('/showall')
def showall():
    # jobs = list(DB.jobs().find())  #оба варианта эквивалентны
    jobs = list(DB.find("jobs"))
    return render_template('jobs.html', jobs=jobs)


# get by query
@bp.route('/byquery')
def byquery():
    myQuery = {"name": "job3"}
    jobs = list(DB.find("jobs", myQuery))
    return render_template('jobs.html', jobs=jobs)


@bp.route('/part')
def part():
    my_list = ["one", list("asd" "dsa"), "three", "four", "five"]
    # return render_template('child.html', my_string="Sample String", my_list=my_list)
    return jsonify({
      "brand": "Ford",
      "model": "Mustang",
      "year": 1964,
      "mylist": my_list
    })

'''
