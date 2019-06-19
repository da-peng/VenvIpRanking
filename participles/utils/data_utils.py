#encoding=utf-8
import time

def get_date():
    current_time = time.strftime('%Y-%m-%d', time.localtime())
    t_list = current_time.split('-')
    current_date = '%d-%d-%d' % (int(t_list[0]), int(t_list[1]), int(t_list[2]))
    return current_date