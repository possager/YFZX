#_*_coding:utf-8_*_
# from YFZX.proxy_to_redis import get_Proxy
from scrapy import cmdline
import threading
from multiprocessing import pool
from YFZX.proxy_to_redis import get_Proxy
import threading
import time
from multiprocessing import pool
import subprocess
import os

#############################################################台海网的数据抓取不完全,


#需要添加的功能:1,定时启动设置,2,关于redis的清空设置,3线程速度控制

# xilu网站是有下一页的（完成）

#自动识别模块部分有bug，title找出来的都是head中的title，不是正文模块中的title，这肯定会导致正文部分找不准，以至于时间寻找部分也找不准


#遗留问题：
#时间的正则查找不是太好，容易找错，而且后向引用没有设置好。
#chengdu网的comment没有设计好，里边很多网页不是手机版的，不过我估计手机版和电脑版的内容有重复，因为今天涛哥打开了一个我一直用手机版网页来看的网页的电脑版。




max_threads=2
SLEEP_TIME=5


def runProxy():
    thread1=threading.Thread(target=get_Proxy,args=())
    thread1.setDaemon()
    thread1.start()
    # thread1.run()

def run_scrapy_spider(spider_name):
    # for i in spider_name:
    #     subprocess.Popen()
    cmdline.execute(('scrapy crawl '+spider_name).split())




def run_multprocess(crawl_queue):
    threads = []
    while threads or crawl_queue:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue:
            # can start some more threads
            spider_name=crawl_queue.pop()
            thread = threading.Thread(target=run_scrapy_spider,args=(spider_name,))
            thread.setDaemon(True)  # set daemon so main thread can exit when receives ctrl-c
            thread.start()
            threads.append(thread)
        # all threads have been processed
        # sleep temporarily so CPU can focus execution on other threads
        time.sleep(SLEEP_TIME)



def run_multprocess2(crawl_queue=None):
    spider_name_list = ['mycdqq', 'sohu']
    pool1=pool.Pool(processes=2)
    pool1.map(run_scrapy_spider,spider_name_list)
    pool1.close()
    pool1.join()



def run_processSpider(crawl_queue):
    subprocess_list=[]
    #F:/project/YFzhongxin/YFZX/YFZX/spiders
    spider_path = '/media/liang/3804CCCA04CC8C76/project/YFzhongxin/YFZX/YFZX/spiders'#/media/liang/3804CCCA04CC8C76/project/YFzhongxin/YFZX/YFZX/spiders
    os.chdir(spider_path)
    while subprocess_list or crawl_queue:
        for subprocess_child in subprocess_list:
            retcode=subprocess_child.poll()
            if not retcode:
                subprocess_list.remove(subprocess_child)
        while len(subprocess_list) < 2 and crawl_queue:
            subprocess_new=subprocess.Popen(['scrapy','crawl',crawl_queue.pop()])
            subprocess_list.append(subprocess_new)
            subprocess_new.wait()






if __name__ == '__main__':
    # spider_name_list=['xilu']
    # run_multprocess(spider_name_list)
    # run_multprocess2()


    # run_processSpider(spider_name_list)

    cmdline.execute('scrapy crawl toutiao'.split())