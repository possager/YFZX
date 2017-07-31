# import random
# import redis
#
# pool1=redis.ConnectionPool(host='localhost',port=6379)
# redis2=redis.Redis(connection_pool=pool1)
#
#
# for i in range(10):
#     testtime=random.randint(1,10)
#     if testtime>5:
#         print redis2


import  requests

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}


# request =requests.get('https://m.toutiao.com/i6439512402986795521/')
session1=requests.session()
response=session1.request(method='get',url='https://m.toutiao.com/i6439512402986795521/',headers=headers)
print response.text