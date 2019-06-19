#encoding=utf-8
import asyncio


def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

def foo():
    print("starting...")
    while True:
        res = yield 4
        print("res:",res)

async def hello():
    print("Hello world!")
    r = await asyncio.sleep(1)
    print("Hello again!")

if __name__ == '__main__':
    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 执行coroutine
    loop.run_until_complete(hello())
    loop.close()
    # c = consumer()
    # produce(c)
    # g = foo()
    # print(next(g))
    # print("*" * 20)
    # print(next(g))# 下一步
    # print(g.send(7))# send是发送一个参数给res的