#_*_coding:utf-8_*_

import requests
import redis
import time
import json
import random
import threading


connectpool=redis.ConnectionPool(host='localhost',port=6379)
redis1=redis.Redis(connection_pool=connectpool)

#首先获得一个proxy的代理池，满了之后暂停一段时间，之后再检擦是否是满的，若不是满的，立即补满。此外，另一个线程不断的从这个originalproxy中读取proxy，再ping百度之后筛选出优质的代理，放入一个优质的代理池中，数量是200个
#没满自动补满。第三个线程维护这个代理池，隔10分钟就扫描一遍。
#将来若是某个某个网站想用这个代理，根据meta中的plant_form中的字段来生成一个新的proxylist
#proxy_





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
    url_to_examing='https://www.baidu.com/'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }

    while redis1.llen('proxy_good')<200:
        proxy1=redis1.lpop('proxy_original')
        session1=requests.session()
        print proxy1
        session1.proxies={
        "http": "http://"+proxy1,
    }
        time1=time.time()
        response1=session1.request(method='get',url=url_to_examing,headers=headers)
        time.sleep(1)
        time2=time.time()
        timeused= time2-time1
        if timeused<3:
            redis1.lpush('proxy_good',proxy1)
            print 'has push one'
    time.sleep(30)

def examing_Proxy():
    while True:
        for i in range(redis1.llen('proxy_good')):
            proxy=redis1.lpop('proxy_good')
            url_to_examing = 'https://www.baidu.com/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
            }
            session2=requests.session()
            session2.proxies={
            "http": "http://"+proxy,
        }
            time1=time.time()
            response1=session2.request(method='get',url=url_to_examing,headers=headers)
            time2=time.time()
            timeused= time2-time1
            # print timeused
            if timeused<5:
                redis1.lpush('proxy_good',proxy)
                print 'has examing one'
        time.sleep(600)

# def examing_Proxy_somewebsite(plant_from):
#     #增加一个字典，来判断应该选取哪一个网站去ping
#
#     url_and_plantform={
#             'sohu': 'https://api.m.sohu.com/autonews/cpool/?n=%E6%96%B0%E9%97%BB&s=0&c=20&dc=1',
#             'newssc': 'http://www.newssc.org/',
#             'xilu': 'http://m.xilu.com/index.html',
#             'chengdu': 'http://wap.chengdu.cn/1700001',
#             # 'taihainet': 5,
#             'toutiao': 'https://www.toutiao.com/api/pc/feed/?max_behot_time=1499133489&category=__all__&utm_source=toutiao&widen=1&tadrequire=false',
#             'mycd_qq': 'http://panda.qq.com/cd/index',
#             'other': 'http://www.baidu.com'
#         }
#     url_to_examing=url_and_plantform[plant_from]
#
#     for i in range(redis1.llen('proxy_good')):
#         proxy = redis1.lpop('proxy_good')
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
#         }
#         session2 = requests.session()
#         session2.proxies = {
#             "http": "http://" + proxy,
#         }
#         time1 = time.time()
#         response1 = session2.request(method='get', url=url_to_examing, headers=headers)
#         time2 = time.time()
#         timeused = time2 - time1
#         if timeused < 5:
#             redis1.lpush(plant_from+'_proxy_good', proxy)
#             print 'has examing one'
#
# def get_proxy_from_plantform(plantform):
#     redis1.lpush(plantform+'_proxy_good')
#
# def send_proxy_back_to_proxylist(proxy,plantform,quantily):
#     #设计时需要处理的问题：1、如果proxylist的长度小于ratio怎么办？再从
#     retio=50
#     redis1.lindex(plantform+'_proxy_good',)




def proxy_sendback(proxy):
    ratio=200
    proxy_at_200=redis1.lindex('proxy_good',ratio)
    redis1.lset('proxy_good',ratio,proxy)
    redis1.rpush('proxy_good',proxy_at_200)






def runProxy():
    thread1=threading.Thread(target=get_Proxy,args=())
    thread2=threading.Thread(target=fillte_Proxy,args=())
    thread3=threading.Thread(target=examing_Proxy,args=())

    thread1.start()
    # thread1.setDaemon()
    # thread1.join()
    thread2.start()
    # thread2.setDaemon()

    thread3.start()
    # thread3.setDaemon()
    
if __name__ == '__main__':
    runProxy()
    