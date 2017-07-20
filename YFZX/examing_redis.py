#_*_coding:utf-8_*_
#这个函数在每次请求回来是检测是否存在了,与另一个redis的代码有区别
import redis

redis_connect_pool=redis.ConnectionPool(host='localhost',port=6379)
redis1=redis.Redis(connection_pool=redis_connect_pool)


def change(key):
    dict1={
        'sohu':1,
        'newssc':2,
        'xilu':3,
        'chengdu':4,
        'taihainet':5,
        'toutiao':6,
        'xinhuanet':7,
        'thepaper':8,
        'mycd_qq':9,

    }
    try:
        return dict1[key]
    except:
        return 100

def creat_url_list_in_redis():
    dict1 = {
        'sohu': 1,
        'newssc': 2,
        'xilu': 3,
        'chengdu': 4,
        'taihainet': 5,
        'toutiao': 6,
        'xinhuanet': 7,
        'thepaper': 8,
        'mycd_qq': 9,
        'other':100

    }
    for i in dict1.iteritems():
        redis1.set(i[1]+i[1],1)
    # redis1.set(plant_form,1)


def exisit(key,value,webname):#这个函数暂时没用了,pagefilter中有正确的功能的代码
    key2=change(key)
    if redis1.exists(webname) and redis1.exists(webname+'_list'):
        if int(redis1.get(webname))<100:
            j=1
            while j:
                j=redis1.rpop(key2)#这里设计错了，pop出来的话那么原列表都空了
                if j==key:

            # if redis1.exists(key):
                    redis1.incr(webname)
                    return 0#已经村咋了
            else:
                try:
                    redis1.lpush(key2,key)
                    return 1
                except:
                    return 9
        else:
            print redis1.get(webname)
            print type(redis1.get(webname))
            return 2

    else:
        redis1.set(webname,0)
        redis1.lpush(key2,0)
        # if key in redis1.get(key):
        #     return 0#已经村咋了
        # else:
        try:
            redis1.lpush(key2,key)
            return 1
        except:
            return 9


if __name__ == '__main__':
    # print exisit('www.baidu.com','2017-12')
    # print redis1.get('wrong_time')
    # print exisit('www.baidu.com','2017-12',webname='wrong_time')
    # print redis1.get('wrong_time')
    creat_url_list_in_redis()