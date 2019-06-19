# encoding=utf-8
from VenvIpRanking.utils.mongodb_connect import *
from VenvIpRanking.models.ip_model import *
from VenvIpRanking.base.base_service import BaseService
import json
import copy

collection = 'proxy_ips'
field = 'ip'

# IP 业务存储逻辑
class IpService(BaseService):


    def __init__(self):
        super().__init__(collection)
        self._ip_list = []
        # print('Ip __init__')

    def insert_ips(self, ip_list):
        '''
        将ip列表存入mongoDB
        :param ip_list:
        :return:
        '''
        # json_ret = json.dumps(list)
        # print(len(list))
        # self._ip_list = ip_list
        # print(id(ip_list))
        # print(id(self._ip_list)) # 传地址
        self._ip_list = copy.copy(ip_list)
        try:
            # 存在则不插入
            exist_ips = self.collection.find({}, {"_id": 0, field: 1})
            for i in exist_ips:
                value = i[field]
                if value in self._ip_list:
                    self._ip_list.remove(value)
            # 如果是[]则返回false
            print('本次新增存储IP为：%s' %self._ip_list)
            if self._ip_list:
                for i in set(self._ip_list):
                    ips = IpsModel(i)
                    # json 数据类型 string
                    data = json.dumps(ips, default=ips.objToJson)

                    data = json.loads(data)
                    # python数据类型

                    self.collection.insert(data)
        except Exception as e:
            print(e)
        finally:
            self.client.close()

    def get_random_ip(self):
        '''
        随机取一个IP
        1. 取出来再check一次，不行就删除再换一个；
        2.
        :return:
        '''




if __name__ == '__main__':

    # test_list = ['116.28.106.165', '110.73.32.6']
    # print(len(test_list))
    # ip_obj = IpService()
    # ip_obj.insert_ips(test_list)
    #
    # print(ip_obj.is_exist('ip', '110.73.32.6'))
    # print(ip_obj.get_count(field))
    # print(ip_obj.select_field(field))
    #
    # ip_obj.remove_value('ip', '110.73.32.6')
    #
    # print(ip_obj.is_exist('ip', '110.73.32.6'))

    l1 = [1,2,[1,2]]

    l2 = copy.copy(l1)
    l3 = copy.deepcopy(l1)
    l1[2][1] = 3
    print(id(l1))
    print(id(l2))
    print(id(l3))
    print(l1)
    print(l2)

    print(l3)
    # print(l4)
    # print('*'*3,l5)
    # l1[2]=[2,3]
    # print(l1)
    # print(l4)
    # print(l5)

    # 函数参数传递
    #不可变对象传值 str int tuple
    #可变对象传地址 list dict
    # 所以要用copy deepcopy
    s = 1
    a = s
    l_1 = [1,2]
    l_2 = l_1 # = 等号是传地址

    print(id(s))
    print(id(a))
    print(id(l_1))
    print(id(l_2))
