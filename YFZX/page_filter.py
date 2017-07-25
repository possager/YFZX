#_*_coding:utf-8_*_
import hashlib
import redis
from YFZX.proxy_to_redis import redis1
# from YFZX.examing_redis import change
import os.path
import os
from YFZX.persionalSetting import BASIC_FILE
####################有时间会有出现timeout故障

class path_to_redis:
    def __init__(self):
        self.basic_file=BASIC_FILE
        self.redis=redis1

    def scan(self,file_path):
        for wenjianjia in os.listdir(file_path):
            if wenjianjia!='speeches':
                if os.path.isdir(file_path+'/'+wenjianjia):
                    self.scan(file_path+'/'+wenjianjia)#递归判断是否是文件夹子如果不是,转到下一个else
                else:
                    wenjianZip_split= wenjianjia.split('_')
                    print wenjianZip_split[0]
                    print wenjianZip_split[3]

                    # num_changed=change(wenjianZip_split[0])
                    name=wenjianZip_split[0]
                    hash_vlaue=wenjianZip_split[3]
                    # self.redis.rpush(num_changed,hash_vlaue)
                    self.redis.hset(name,hash_vlaue,1)#这里的1是随便设置的

    def examing(self,url_to_exam,plantform):#用来检测链接时候爬取过的表
        # key2=change(plantform)
        key2=plantform
        # List_redis=self.redis.get(key2)
        # print List_redis
        # for i in range(self.redis.llen(key2)):
        #     print self.redis.lindex(key2,i)
        hash_url=str(hashlib.md5(url_to_exam).hexdigest())
        result_num=self.redis.hset(key2+'_has_crawled',hash_url,1)
        return result_num

    def creat_url_list_in_redis(self):#用来存放重复次数是否超过100次的那个列表
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
            'other': 100
        }
        for i in dict1.iteritems():
            redis1.set(i[0], 1)
            # redis1.set(plant_form,1)


if __name__ == '__main__':
    thisclass=path_to_redis()
    # thisclass.Init()
    # thisclass.scan(BASIC_FILE)
    # result_num=thisclass.examing(url_to_exam='http://panda.qq.com/cd/interface/topic/getRecThreads?s_code=&page=1&pagesize=10',plantform='sohu')
    # print result_num
    # thisclass.examing('baidu.com','sohu')


    thisclass.creat_url_list_in_redis()
    # thisclass.examing('baidu.com','baidu')