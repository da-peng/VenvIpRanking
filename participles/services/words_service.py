# encoding=utf-8
from VenvIpRanking.utils.mongodb_connect import *
import json
import pandas as pd
import jieba
import re


# VLog视频分词汇总
class WordServices(object):

    def __init__(self, collection):
        self.client = MongoUtil().client
        self.collection = MongoUtil().db[collection]

    def split_word(self):
        titles = self.collection.find({}, {"_id": 0, "title": 1})
        data = pd.DataFrame(list(titles))
        # print(title1)
        # print(re.split('/|：',title1))
        punctuation = """！＂＃＄％＆＇（）＊＋－／＜＝＞＠《［＼］＾＿｀(≧▽≦).｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏"""
        word = []
        for title in data['title'].values:
            re_punctuation = "[{}]+".format(punctuation)
            title = re.sub(re_punctuation, "", title)

            split_list = re.split('/|：|，|？|-|\||', title)
            if (len(split_list) > 1):
                word.append(list(filter(None, split_list)))
            else:
                obj = jieba.cut(title, cut_all=False)
                word.append(list(filter(None, obj)))
        self.client.close()
        return word


    def store_words(self,word):
        data_frame = {'words': word}
        df = pd.DataFrame(data_frame)
        self.collection.insert(json.loads(df.T.to_json()).values())
        self.client.close()






# seg_list = jieba.cut(title, cut_all=False)
# print(list(seg_list))
# dicts = {'one': [1, 2, 3], 'two': [2, 3, 4], 'three': [3, 4, 5]}
# df = pd.DataFrame(dicts)
# wordService.collection.insert(json.loads(df.T.to_json()).values())
# wordService.client.close()
# print(json.loads(df.T.to_json()).values())
