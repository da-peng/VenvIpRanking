#encoding=utf-8


class IpsModel(object):

    def __init__(self,ip):
        self.ip = []
        # if isinstance(ip,list):
        #     for i in ip:
        #         self.ip.append(i)
        # else:
        self.ip = ip

    def objToJson(self,obj_instance):

        return {
            'ip':obj_instance.ip
        }

    def jsonToObj(json):

        return IpsModel(json['ip'])
