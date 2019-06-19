# encoding=utf-8
from VenvIpRanking.utils.mongodb_connect import *
import json
import pandas as pd



class TagHeatServices(object):
    '''
    标签热度
    '''

    def __init__(self, collection):
        self.client = MongoUtil().client
        self.collection = MongoUtil().db[collection]

    def get_data(self):
        data = self.collection.find({}, {"_id": 0, "__v": 0, "updata_time": 0, "video_slink": 0})
        self.data_frame = pd.DataFrame(data)
        # print(self.data_frame.columns.values.tolist())

    def get_author_watch_num(self):
        author_watch_num = self.data_frame.groupby(["author", "author_home_link"])["watch_num"].sum()

        return author_watch_num.to_frame().sort_values(['watch_num'], ascending=False)

    def get_tag_name_count(self):
        get_tag_name_count = self.data_frame["tag_name"]
        return get_tag_name_count

    def store_words(self, df):
        # data_frame = {'words': word}
        # df = pd.DataFrame(data_frame)
        self.collection.insert(json.loads(df.T.to_json()).values())
        self.client.close()


if __name__ == '__main__':
    pass
