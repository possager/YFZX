#_*_coding:utf-8_*_
import redis

redis_connect_pool=redis.ConnectionPool(host='localhost',port=6379)
redis1=redis.Redis(connection_pool=redis_connect_pool)



def exisit(key,value,webname):
    if redis1.exists(webname):
        if int(redis1.get(webname))<100:
            if redis1.exists(key):
                redis1.incr(webname)
                return 0#已经村咋了
            else:
                try:
                    redis1.set(key,value)
                    return 1
                except:
                    return 9
        else:
            print redis1.get(webname)
            print type(redis1.get(webname))
            return 2

    else:
        redis1.set(webname,0)
        if redis1.exists(key):
            return 0#已经村咋了
        else:
            try:
                redis1.set(key,value)
                return 1
            except:
                return 9
