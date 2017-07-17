#_*_coding:utf-8_*_
import hashlib
import redis
from YFZX.proxy_to_redis import redis1
from YFZX.examing_redis import change
import os.path
import os
from YFZX.persionalSetting import BASIC_FILE


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

                    num_changed=change(wenjianZip_split[0])
                    hash_vlaue=wenjianZip_split[3]
                    self.redis.rpush(num_changed,hash_vlaue)


    def examing(self,url_to_exam,plantform):
        key2=change(plantform)
        # List_redis=self.redis.get(key2)
        # print List_redis
        for i in range(self.redis.llen(key2)):
            print self.redis.lindex(key2,i)


if __name__ == '__main__':
    thisclass=path_to_redis()
    # thisclass.Init()
    # thisclass.scan(BASIC_FILE)
    thisclass.examing(url_to_exam='http://panda.qq.com/cd/interface/topic/getRecThreads?s_code=&page=1&pagesize=10',plantform='sohu')