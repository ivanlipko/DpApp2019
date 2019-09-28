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
import pymongo

class DB(object):

    @staticmethod
    def init(URI):
        # client = pymongo.MongoClient(URI, username='admin', password='admin', authSource='test', authMechanism='SCRAM-SHA-1')
        client = pymongo.MongoClient(URI)
        DB.DATABASE = client['test']

    @staticmethod
    def insert(collection, data):
        DB.DATABASE[collection].insert(data)

    @staticmethod
    def find_one(collection, query):
        return DB.DATABASE[collection].find_one(query)

    @staticmethod
    def find(collection, query={}):
        return DB.DATABASE[collection].find(query)

    @staticmethod
    def jobs():
        return DB.DATABASE["jobs"]
