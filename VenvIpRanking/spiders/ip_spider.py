# encoding=utf-8
import asyncio
import scrapy, requests, time, aiohttp
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count
from VenvIpRanking.services.ip_service import IpService

test_url = 'http://httpbin.org/ip'


class IpSpider(scrapy.Spider):
    name = "venv_ip"

    def start_requests(self):
        urls = [
            'https://www.xicidaili.com/',
            # 'https://search.bilibili.com/all?keyword=Vlog&from_source=banner_search'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
        爬取IP列表 https://www.xicidaili.com/
        :param response:
        :return:
        '''
        page = response.url.split("/")[-2]
        self.filename = 'venv_ip-%s.html' % page

        with open(self.filename, 'wb') as f:
            f.write(response.body)
        # 创建文件保存响应的html
        self.log('Saved file %s' % self.filename)
        self.ip_list = []
        self.port = []
        # 查看爬取的IP列表
        with open(self.filename) as fp:
            soup = BeautifulSoup(fp)
        ip_table = soup.find_all('table', id='ip_list')
        items = ip_table[0].find_all('tr', class_='odd')
        print(len(items))
        count = 1
        for i in items:

            ip = i.find_all('td')[1].get_text()
            port = i.find_all('td')[2].get_text()
            self.ip_list.append(ip + ':' + port)
            count += 1
            if count >= 40:
                break
        # 检查IP是否可用
        # 请求http://httpbin.org/ip check response字段

        t1 = time.time()
        loop = asyncio.get_event_loop()  # event_loop -> task
        loop.run_until_complete(self.create_task(loop, test_url, self.ip_list))
        loop.close()
        print("Async total time:", time.time() - t1)

        # check_ret = self.pool_check(test_url)
        check_ret = []

        for i in self.all_results:
            if i is not None:
                check_ret.append(i)
        print('check 结果：%s' %check_ret)
        if check_ret:
            ip_obj = IpService()
            ip_obj.insert_ips(check_ret)

    def pool_check(self, url_for_test):
        '''
        进程池启动
        :param url_for_test:
        :return:
        '''
        # print(self.ip_list)
        # 使用进程池发送请求
        pool = Pool(cpu_count() - 2)
        current = time.time()
        results = []
        for ip_info in self.ip_list:
            results.append(pool.apply_async(self.ip_check, (url_for_test, ip_info)))
        pool.close()
        pool.join()

        tmp = []
        for i in results:
            if i.get() is not None:
                tmp.append(i.get())
        end_time = time.time()
        use_time = end_time - current
        print('测试耗时：%d s' % use_time)
        print('测试结果：%s' % tmp)
        return tmp

    async def async_check_ip(self, client, url, ip):
        proxy_url = 'http://' + ip
        # print(proxy_url)
        try:
            resp = await client.get(url, proxy=proxy_url, timeout=10)
            # print(resp.status)
            if resp.status == 200:
                print(await resp.text())
                return ip
        except Exception as e:
            return

    async def create_task(self, loop, url, ip_list):
        async with aiohttp.ClientSession() as client:
            tasks = [loop.create_task(self.async_check_ip(client, url, ip)) for ip in ip_list]
            finished, unfinished = await asyncio.wait(tasks)
            self.all_results = [r.result() for r in finished]
            # print(self.all_results)
            # return all_results

    def parse_coroutine(self):
        '''
         尝试使用协程
         缺点明显
         1.无法利用多核资源，协程的本质是个单线程,它不能同时将 单个CPU 的多个核用上
         2.有一处进行阻塞操作（如IO时）会阻塞掉整个程序
        :return:
        '''
        self.ip_info = []
        s = self.ip_check_coroutine(test_url)
        s.send(None)
        for i in self.ip_list:
            s.send(i)
        print('测试结果：%s' % self.ip_info)
        if self.ip_info:
            ip_obj = IpService()
            ip_obj.insert_ips(self.ip_info)

    def ip_check_coroutine(self, url_for_test):
        while True:
            ip_info = yield
            proxies = {
                'http': 'http://' + ip_info,
                'https': 'https://' + ip_info,
            }
            try:
                r = requests.get(url_for_test,
                                 proxies=proxies, timeout=20)
                if r.status_code == 200:
                    print('测试通过')
                    print(r.text)
                    self.ip_info.append(ip_info)
            except Exception as e:
                print(e)

    # 坑 Pool 这里要用类方法，不能用实例方法,实例测试了一下无法进行进程间传递；不同的内存空间
    @classmethod
    def ip_check(cls, url_for_test, ip_info):
        '''
        测试ip是否可用
        :param url_for_test:
        :param ip_info:
        :return:
        '''
        # 设置代理
        proxies = {
            'http': 'http://' + ip_info,
            'https': 'https://' + ip_info,
        }
        try:
            print({'ip': ip_info})
            response = requests.get(url_for_test,
                                    proxies=proxies, timeout=10)
            if response.status_code == 200:
                # print('测试通过')
                # print(response.text)
                return ip_info
            else:
                # print('请求失败')
                pass
        except Exception as e:
            # print('超时失败')
            pass


if __name__ == '__main__':
    # pool = Pool(cpu_count() - 2)
    # # print(list(range(10)))
    # for ip_info in range(10):
    #     # print(ip_info)
    #     current = time.time()
    #     pool.apply_async(f,(ip_info,))
    #     # pool.start()
    #     # pool.join()
    #     endTime = time.time()
    #     useTime = endTime - current
    #     print('测试耗时：%d' % useTime)
    # #
    # pool.close()
    # pool.join()
    # ip_list = ['123.163.96.194', '123.163.96.191']
    test_url = 'http://www.baidu.com'
    ipSpider = IpSpider()
    t1 = time.time()
    loop = asyncio.get_event_loop()  # event_loop -> task
    loop.run_until_complete(ipSpider.create_task(loop, test_url))
    loop.close()
    print("Async total time:", time.time() - t1)
