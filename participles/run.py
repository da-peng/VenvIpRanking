# encoding=utf-8
import time
from participles.services.words_service import WordServices
from participles.services.tag_author_heat import TagHeatServices
from participles.utils.data_utils import get_date
import pandas as pd

current_date = get_date()


def analysis_word():
    for i in ['composite', 'most_clickrate', 'new_publish', 'most_dm', 'most_collect']:
        title_data = WordServices('vlog_info_' + i + '_' + current_date)
        split_words = title_data.split_word()
        # 保存数据
        store_words = WordServices('words_' + current_date)
        store_words.store_words(split_words)


def analysis_up_heat():
    series_author_watch_num = []
    series_tag_name_watch_num = []
    for i in ['composite', 'most_clickrate', 'new_publish', 'most_dm', 'most_collect']:
        tag = TagHeatServices('vlog_info_' + i + '_' + current_date)
        tag.get_data()

        author_watch_num = tag.get_author_watch_num()

        series_author_watch_num.append(author_watch_num)

        get_tag_name_watch_num = tag.get_tag_name_count()
        series_tag_name_watch_num.append(get_tag_name_watch_num)
    result1 = pd.concat(series_author_watch_num, axis=0)
    result = result1.groupby('author')['watch_num'].sum().to_frame().reset_index() \
        .sort_values(['watch_num'], ascending=False)
    '''
    1.坑1。需要Series到Frame 互转恶心死人，还有columns没有实际加上
    '''
    result2 = (pd.concat(series_tag_name_watch_num, axis=0))
    result3 = (result2.to_frame()).groupby(['tag_name'])['tag_name'].count().reset_index(name="count")
    result4 = result3.sort_values(['count'], ascending=False)
    # 保存数据
    tag1 = TagHeatServices('tag_name_watch_num_' + current_date)
    tag1.store_words(result4)
    tag2 = TagHeatServices('author_watch_num_' + current_date)
    tag2.store_words(result)


if __name__ == '__main__':
    analysis_word()
    analysis_up_heat()
