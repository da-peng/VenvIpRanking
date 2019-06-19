#encodingf=utf-8
import time
from participles.services.tag_author_heat import TagHeatServices

'''
设计有些不合理
'''
if __name__ == '__main__':
    current_time = time.strftime('%Y-%m-%d', time.localtime())

    for i in range(2):
        tag = TagHeatServices('current_time')
