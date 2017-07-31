#_*_coding:utf-8_*_

import requests
import time
import re
import redis


pool1=redis.ConnectionPool(host='localhost',port=6379)
redis1=redis.Redis(connection_pool=pool1)


while True:
        for i in range(300):
                if redis1.llen('111') < 200:
                        redis1.lpush('111',i)
                else:
                        time.sleep(5)