#encoding=utf-8
from multiprocessing import Pool,cpu_count


class Runner(object):
    def __init__(self):
        self.pool = Pool(cpu_count()-2)
        self.result = []



if __name__ == '__main__':

    run = Runner()
    