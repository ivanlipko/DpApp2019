#!/usr/bin/env python
# coding=utf-8

from flask import Flask

from app.database import DB
from app.models.mappoint import mapPoint


def create_app(config):
    app = Flask(__name__)
    app.config.from_pyfile('server.cfg')
    #app.config['TESTING'] = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    DB.init(app.config['DATABASE_URI'])
    print(app.config['DATABASE_URI'])
    register_blueprints(app)
#    for job_name in ['job1', 'job2', 'job3']:
#        new_job = mapPoint(operator=job_name)
#        new_job.insert()
    return app


def register_blueprints(app):

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)


if __name__ == '__main__':
    print('Running api server...')

    app = Flask(__name__)
    app.config.from_pyfile('server.cfg')
    app.config['TESTING'] = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True

    DB.init(app.config['DATABASE_URI'])
    register_blueprints(app)
    # for job_name in ['job1', 'job2', 'job3']:
    #     new_job = mapPoint(operator=job_name)
    #     new_job.insert()
    # return app

    # app.run("localhost", "9999", debug=True)
    app.run("0.0.0.0", "9999", debug=True)
    # app.run("0.0.0.0", "8080", debug=True)
    # app.run("localhost", "9999")

# start mongo
# mongod --dbpath ~/data/db/
