# #coding:UTF-8
# import time
#
# dt = "2016-05-05 20:28:54"
#
# #转换成时间数组
# timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
# #转换成新的时间格式(20160505-20:28:54)
# dt_new = time.strftime("%Y%m%d-%H:%M:%S",timeArray)
#
# print dt_new

import datetime
import time
import requests


# time_type='%Y_%m_%d %X'
# print time.strftime(time_type,time.localtime())
# print str(int(time.time()))
# print str(None)
#

session=requests.session()
# requests1=requests.Request(method='post',url='http://m.xilu.com/index.html',data={'page':4})

headers={
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Referer':'http://m.xilu.com/index.html',
    'Origin':'http://m.xilu.com',
    'Host':'m.xilu.com',
    'Cookie':'__cfduid=d352207b89afbb736905d84c746bd629e1498708887; Hm_lvt_82517de1aba077f27b656b61d72a310c=1499326583; tma=170456873.47460727.1499326583007.1499326583007.1499326583007.1; tmd=1.170456873.47460727.1499326583007.; fingerprint=0a7ae531e3d89881730a7dc5bc7fbbd7; bfd_g=846102420a015a0e0000313f0000ea8859375784; cn_2f15e0c2c6917b9d45c5_dplus=%7B%22distinct_id%22%3A%20%2215d16d4111f34c-054d678d29b893-38750f56-1fa400-15d16d41120759%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201499326584%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201499326584%7D; UM_distinctid=15d16d4111f34c-054d678d29b893-38750f56-1fa400-15d16d41120759; _csrf=5a1c72cce6d457c0c6b71e1aeccbecd12a007ff1139058a81b07ea78ed27438fa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22deCb9Y_7K5NMexR9TUV25TDbx9KjdUxe%22%3B%7D; cnzz_lsdcs=1; Hm_lpvt_cedd8cbdba88d7634e913e59678c37f4=1499330190; Hm_lvt_cedd8cbdba88d7634e913e59678c37f4=1499330190',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Content-Length':'6',
    'Connection':'keep-alive',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept':'application/json, text/javascript, */*; q=0.01'
}


headers2 = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
            # 'X-Requested-With':'XMLHttpRequest',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'m.xilu.com',
            'Upgrade-Insecure-Requests':'1',
            # 'Cookie': '__cfduid=d352207b89afbb736905d84c746bd629e1498708887; Hm_lvt_82517de1aba077f27b656b61d72a310c=1499326583; tma=170456873.47460727.1499326583007.1499326583007.1499326583007.1; tmd=1.170456873.47460727.1499326583007.; fingerprint=0a7ae531e3d89881730a7dc5bc7fbbd7; bfd_g=846102420a015a0e0000313f0000ea8859375784; cn_2f15e0c2c6917b9d45c5_dplus=%7B%22distinct_id%22%3A%20%2215d16d4111f34c-054d678d29b893-38750f56-1fa400-15d16d41120759%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201499326584%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201499326584%7D; UM_distinctid=15d16d4111f34c-054d678d29b893-38750f56-1fa400-15d16d41120759; _csrf=5a1c72cce6d457c0c6b71e1aeccbecd12a007ff1139058a81b07ea78ed27438fa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22deCb9Y_7K5NMexR9TUV25TDbx9KjdUxe%22%3B%7D; cnzz_lsdcs=1; Hm_lpvt_cedd8cbdba88d7634e913e59678c37f4=1499330190; Hm_lvt_cedd8cbdba88d7634e913e59678c37f4=1499330190',
    'Referer': 'http://m.xilu.com/index.html',

}

data1=session.request(method='post',url='http://m.xilu.com/v/1000010000998952.html',data={'page':4},headers=headers2,cookies={})
print data1.text

# import bitmap
# class Bitmap(object):
#     def __init__(self,max):
#         self.size=int((max+31-1)/31)

# if __name__ == '__main__':
#     bitmap1=Bitmap(90)
#     print bitmap1.size


# -*- coding:utf-8 -*-

import os
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')
#
# import random
#
# from pybloomfilter import BloomFilter
#
# # 申请一个内存等于1M的容器，错误率等于0.001的bloomfilter对象
# bfilter = BloomFilter(1 * 1024 * 1024, 0.001)
#
# # 添加100万个元素
# for x in xrange(1000000):
#     bfilter.add(str(x))
#
# # 测试错误率
# error_in = 0
# for x in xrange(2000000):
#     if str(x) in bfilter and x > 1000000:
#         error_in += 1
#
# print "error_rate:%s" % (error_in * 1.0 / 1000000)

# print ['x------>'+str(i) for i in range(10,20)]