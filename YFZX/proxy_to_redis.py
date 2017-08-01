#_*_coding:utf-8_*_


# import requests
# import redis
# import json
# import time
# import random
#
# #公司的购买的代理
# #一般的代理http://svip.kuaidaili.com/api/getproxy/?orderid=953994536123042&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&sp1=1&quality=2&sort=1&format=json&sep=1
# #http://svip.kuaidaili.com/api/getproxy/?orderid=953994536123042&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&quality=2&format=json&sep=1
# #http://dps.kuaidaili.com/api/getdps/?orderid=940097016277555&num=50&ut=1&sep=1
# ################################这个是一般的
#
# #公司购买的私密代理
# #http://dps.kuaidaili.com/api/getdps/?orderid=940097016277555&num=50&ut=1&format=json&sep=1
# #################################这个是好用的，但是ip变了，还需要验证登陆
#
#
# pool1=redis.ConnectionPool(host='localhost',port=6379)
# redis1=redis.Redis(connection_pool=pool1)
#
#
# def get_Proxy():
#     headers={
#         'Accept-Encoding': 'gzip'
#     }
#     def get_proxy_to_redis():
#         session1=requests.session()
#         proxy_url='http://svip.kuaidaili.com/api/getproxy/?orderid=953994536123042&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&sp1=1&quality=2&sort=1&format=json&sep=1'
# ################################这个是一般的'
#         webdata=session1.request(method='GET',url=proxy_url,headers=headers)
#         # print webdata
#         data_json=json.loads(webdata.text)
#         print data_json
#         # print data_json
#         for proxyip in data_json['data']['proxy_list']:
#             print proxyip
#             # redis1.rpush('999',proxyip)
#             redis1.lpush('999',proxyip)#左进右出
#     get_proxy_to_redis()
#     while True:
#         while redis1.llen('999') < 300:
#             time.sleep(random.randint(1,3))
#             get_proxy_to_redis()
#
#
#
# def get_proxy_from_redis():
#     # return redis1.hget()
#     #730增加当队列为空的时候的一个等待操作
#     while redis1.llen('999')<10:
#         print 'proxy pool in redis is fewer than 10,please examing reids pool'
#         time.sleep(2)
#     return redis1.rpop('999')
#
# def test_proxy():
#     session2=requests.session()
#     session2.proxies={'http':'http://'+get_proxy_from_redis()}
#     data=session2.request(method='GET',url='http://www.baidu.com')
#     print data.text
#
# if __name__ == '__main__':
#     get_Proxy()
#     # print get_proxy_from_redis()
#     # test_proxy()

# _*_coding:utf-8_*_

import requests
import redis
import time
import json
import random
import threading
from multiprocessing import process



connectpool = redis.ConnectionPool(host='localhost', port=6379)
redis1 = redis.Redis(connection_pool=connectpool)


# 首先获得一个proxy的代理池，满了之后暂停一段时间，之后再检擦是否是满的，若不是满的，立即补满。此外，另一个线程不断的从这个originalproxy中读取proxy，再ping百度之后筛选出优质的代理，放入一个优质的代理池中，数量是200个
# 没满自动补满。第三个线程维护这个代理池，隔10分钟就扫描一遍。
# 将来若是某个某个网站想用这个代理，根据meta中的plant_form中的字段来生成一个新的proxylist
# proxy_





def get_Proxy():
    headers = {
        'Accept-Encoding': 'gzip'
    }

    def get_proxy_to_redis():
        session1 = requests.session()
        proxy_url = 'http://svip.kuaidaili.com/api/getproxy/?orderid=953994536123042&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&sp1=1&quality=2&sort=1&format=json&sep=1'
        ################################这个是一般的'
        webdata = session1.request(method='GET', url=proxy_url, headers=headers)
        # print webdata
        data_json = json.loads(webdata.text)
        print data_json
        # print data_json
        for proxyip in data_json['data']['proxy_list']:
            print proxyip
            redis1.lpush('proxy_original', proxyip)  # 左进右出

    get_proxy_to_redis()
    while True:
        while redis1.llen('proxy_original') < 300:
            time.sleep(random.randint(1, 3))
            get_proxy_to_redis()


def fillte_Proxy():
    url_to_examing = 'https://www.baidu.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    while True:
        while redis1.llen('proxy_good') < 600:
            proxy1 = redis1.lpop('proxy_original')
            session1 = requests.session()
            print proxy1
            session1.proxies = {
                "http": "http://" + proxy1,
            }
            time1 = time.time()
            response1 = session1.request(method='get', url=url_to_examing, headers=headers)
            time.sleep(1)
            time2 = time.time()
            timeused = time2 - time1
            if timeused < 3:
                redis1.rpush('proxy_good', proxy1)
                print 'has push one,timeused is ',timeused
        time.sleep(30)

def mult_thread_to_fillte_Proxy():
    print ''
    threadlist = []
    # while redis1.llen('proxy_good') < 600 or threadlist:
    #     for one in threadlist:
    #         if not one.is_alive():
    #             threadlist.remove(one)
    #     while len(threadlist) < 5 and threadlist:
    while len(threadlist)<5:
        thread_to_examproxy=threading.Thread(target=fillte_Proxy,args=())
        threadlist.append(thread_to_examproxy)
    for i in threadlist:
        i.start()
    while len(threadlist)>1:
        pass



def examing_Proxy():
    while True:
        for i in range(redis1.llen('proxy_good')):
            proxy = redis1.lpop('proxy_good')
            url_to_examing = 'https://www.baidu.com/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
            }
            session2 = requests.session()
            session2.proxies = {
                "http": "http://" + proxy,
            }
            time1 = time.time()
            response1 = session2.request(method='get', url=url_to_examing, headers=headers)
            time2 = time.time()
            timeused = time2 - time1
            # print timeused
            if timeused < 5:
                redis1.lpush('proxy_good', proxy)
                print 'has examing one'
        time.sleep(60)


def get_proxy_from_redis():
    return redis1.lpop('proxy_good')


def proxy_sendback(proxy):
    ratio = 200
    proxy_at_200 = redis1.lindex('proxy_good', ratio)
    redis1.lset('proxy_good', ratio, proxy)
    redis1.rpush('proxy_good', proxy_at_200)


def runProxy():
    thread1 = threading.Thread(target=get_Proxy, args=())
    thread2 = threading.Thread(target=fillte_Proxy, args=())
    thread3 = threading.Thread(target=examing_Proxy, args=())

    thread1.start()
    # thread1.setDaemon()
    thread2.start()
    # thread2.setDaemon()
    thread3.start()
    # thread3.setDaemon()


if __name__ == '__main__':
    process1=process.Process(target=mult_thread_to_fillte_Proxy,args=())
    thread1 = threading.Thread(target=get_Proxy, args=())
    thread2 = threading.Thread(target=fillte_Proxy, args=())
    thread3 = threading.Thread(target=examing_Proxy, args=())

    thread1.start()
    # thread1.setDaemon()
    time.sleep(5)
    # thread2.start()
    # thread2.setDaemon()
    process1.start()
    process1.join()
    thread3.start()
    # thread3.setDaemon()
