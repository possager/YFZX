import redis



pool1=redis.ConnectionPool(host='localhost', port=6379)
redis1=redis.Redis(connection_pool=pool1)



# for ll in range(5,15):
#     print redis1.hset('llde',ll,2)
# print redis1.hlen('llde')
# print redis1.hget('llde',5)
#
# print redis1.lpush('one',1)
# print redis1.rpop('one')
# print redis1.lpush('one','one')
# print redis1.lrange('one',0,100)


print redis1.hset('newssc_has_crawled','www.baidu.com','2')