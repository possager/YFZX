#_*_coding:utf-8_*_
from YFZX.proxy_to_redis import get_Proxy
from scrapy import cmdline
import threading
from multiprocessing import pool
from YFZX.proxy_to_redis import get_Proxy



thread1=threading.Thread(target=get_Proxy,args=())
cmdline.execute('scrapy crawl mycdqq'.split())