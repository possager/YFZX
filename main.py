#_*_coding:utf-8_*_
from YFZX.proxy_to_redis import get_Proxy
from scrapy import cmdline
import threading
from multiprocessing import pool



cmdline.execute('scrapy crawl mycdqq'.split())