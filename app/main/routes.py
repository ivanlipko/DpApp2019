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
from app.models.mappoint import mapPoint, collection_mapPoints
from app.database import DB
from flask import jsonify


def del_obj_id(point):
    # task['_id'] = 0
    point['_id'] = str(point['_id'])
    return point


@bp.route('/')
def index():
    """Main page route."""
    #button_text = "Add Job"
    #return render_template('main.html', button_text=button_text)
    return render_template('index.html')

'''
добавляем новую точку, поле operator - обязательное
curl -i -H "Content-Type: application/json" -X POST -d '{"operator":"mts", "lat":"44.53", "long":"39.56", "power":"-45.0", "network_type":"3g", "_id":"1"}' http://localhost:9999/add_point
curl -i -H "Content-Type: application/json" -X POST -d '{"operator":"tele2", "lat":"42.5876453", "long":"39.234556", "power":"-35.0", "network_type":"4g", "_id":"1"}' http://localhost:9999/add_point
curl -i -H "Content-Type: application/json" -X POST -d '{"operator":"megafon", "lat":"41.34553", "long":"33.45956", "power":"-55.0", "network_type":"3g", "_id":"1"}' http://localhost:9999/add_point
curl -i -H "Content-Type: application/json" -X POST -d '{"operator":"megafon", "lat":"44.34534553", "long":"32.12356", "power":"-25.0", "network_type":"2g", "_id":"1"}' http://localhost:9999/add_point

'''
@bp.route('/add_point', methods=['POST'])
def add_point():
    """Adds point to the database."""
    if not request.json or not 'operator' in request.json:
        abort(400)
    new_point = mapPoint(
        operator=request.json.get('operator', ''),
        lat=request.json.get('lat', ''),
        long=request.json.get('long', ''),
        power=request.json.get('power', ''),
        network_type=request.json.get('network_type', ''),
        id1=request.json.get('id', '')
    )
    new_point.insert()
    return jsonify(new_point.json()), 201


"""
get ALL collection_mapPoints of elements

получить список всех точек
curl -i http://localhost:9999/showall

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
curl -i -H "Content-Type: application/json" -X GET -d '{ "query": {"operator":"megafon"} }' http://localhost:9999/show

curl -i -H "Content-Type: application/json" -X GET -d '{ "query": {"operator":"mts"} }' http://localhost:9999/show

берём все точки, где тип сети 4g
curl -i -H "Content-Type: application/json" -X GET -d '{ "query": {"network_type":"4g"} }' http://localhost:9999/show

берём все точки, где тип сети 4g или 2g
curl -i -H "Content-Type: application/json" -X GET -d '{"query": {"network_type":{"$in":["4g","2g"]}} }' http://localhost:9999/show

берём все точки, где мощность сигнала больше
curl -i -H "Content-Type: application/json" -X GET -d '{"query": {"power":{"$lt":40}} }' http://localhost:9999/show

'''
@bp.route('/show', methods=['GET'])
def show_point():
    print('vot:')
    operator = request.args.get('operator')
    print(operator)


    if not request.json or not 'query' in request.json:
        abort(400)
    query = request.json.get('query', '')
    points = [doc for doc in DB.find(collection_mapPoints, query=query)]
    points = list(map(del_obj_id, points))
    return jsonify(points), 200


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
