#encoding=utf-8

from pymongo import  *

connect_url = 'mongodb://localhost:27017/'
db_name = 'test'

class MongoUtil(object):

    def __init__(self):
        self.client = MongoClient(connect_url)
        self.db = self.client[db_name]

    def __new__(cls, *args, **kwargs):

        if not hasattr(cls,'_instance'):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

