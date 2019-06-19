#encoding=utf-8
class WordsModel(object):

    def __init__(self,word,weight):
        self.word = word
        # if isinstance(ip,list):
        #     for i in ip:
        #         self.ip.append(i)
        # else:
        self.weight = weight

    def objToJson(self,obj_instance):

        return {
            'word':obj_instance.word,
            'weight': obj_instance.weight
        }

    def jsonToObj(json):

        return WordsModel(json['word'],json['weight'])
