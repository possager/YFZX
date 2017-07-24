#_*_coding:utf-8_*_

import redis


connectPool=redis.ConnectionPool(host='localhost',port=6379)
redis1=redis.Redis(connection_pool=connectPool)

# redis1.hset(name='newssc_has_crawled',key='one',value=1)

print redis1.hset('newwsc'+'_has_crawled','www.baidu.com',3)
print redis1.hset('newssc_has_crawled','www.baidu.com','2')