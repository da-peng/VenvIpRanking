# encoding=utf-8
from VenvIpRanking.utils.mongodb_connect import *

# 公用业务方法
class BaseService(object):

    def __init__(self, collection):
        self.client = MongoUtil().client
        self.collection = MongoUtil().db[collection]
        # print('Base __init__')

    def is_exist(self, column, value):
        exist_ips = self.collection.find({}, {"_id": 0, column: 1})
        for i in exist_ips:
            data = i[column]
            if data == value:
                return True
        return False

    def get_count(self, column):
        return self.collection.find({}, {"_id": 0, column: 1}).count()

    def select_field(self, column):
        exist_ips = self.collection.find({}, {"_id": 0, column: 1})
        result = []
        for i in exist_ips:
            result.append(i[column])
        return result

    def remove_value(self, field, value):
        self.collection.remove({field: value})
