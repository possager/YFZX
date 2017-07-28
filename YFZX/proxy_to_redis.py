#_*_coding:utf-8_*_
import requests
import redis
import json
import time
import random

#公司的购买的代理
#http://svip.kuaidaili.com/api/getproxy/?orderid=953994536123042&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&quality=2&format=json&sep=1
#http://dps.kuaidaili.com/api/getdps/?orderid=940097016277555&num=50&ut=1&sep=1
################################这个是一般的

#公司购买的私密代理
#http://dps.kuaidaili.com/api/getdps/?orderid=940097016277555&num=50&ut=1&format=json&sep=1
#################################这个是好用的，但是ip变了，还需要验证登陆


pool1=redis.ConnectionPool(host='localhost',port=6379)
redis1=redis.Redis(connection_pool=pool1)


def get_Proxy():
    headers={
        'Accept-Encoding': 'gzip'
    }
    def get_proxy_to_redis():
        session1=requests.session()
        proxy_url='http://svip.kuaidaili.com/api/getproxy/?orderid=953994536123042&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_an=1&an_ha=1&sp1=1&quality=2&format=json&sep=1'
################################这个是一般的'
        webdata=session1.request(method='GET',url=proxy_url,headers=headers)
        # print webdata
        data_json=json.loads(webdata.text)
        print data_json
        # print data_json
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