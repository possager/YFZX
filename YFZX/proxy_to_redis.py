#_*_coding:utf-8_*_
import requests
import redis
import json
import time
import random




pool1=redis.ConnectionPool(host='localhost',port=6379)
redis1=redis.Redis(connection_pool=pool1)


def get_Proxy():

    def get_proxy_to_redis():
        session1=requests.session()
        proxy_url='http://dps.kuaidaili.com/api/getdps/?orderid=940097016277555&num=50&ut=1&format=json&sep=1 '
        webdata=session1.request(method='GET',url=proxy_url)
        data_json=json.loads(webdata.text)
        for proxyip in data_json['data']['proxy_list']:
            print proxyip
            # redis1.rpush('999',proxyip)
            redis1.lpush('999',proxyip)#左进右出
    get_proxy_to_redis()
    while True:
        while redis1.llen('999') < 300:
            time.sleep(random.randint(1,3))
            get_proxy_to_redis()



def get_proxy_from_redis():
    # return redis1.hget()
    return redis1.rpop('999')

def test_proxy():
    session2=requests.session()
    session2.proxies={'http':'http://'+get_proxy_from_redis()}
    data=session2.request(method='GET',url='http://www.baidu.com')
    print data.text

if __name__ == '__main__':
    get_Proxy()
    # print get_proxy_from_redis()
    # test_proxy()