#_*_coding:utf-8_*_

import requests
import time
import re


session1=requests.session()
response_data=session1.request(method='GET',url='http://wap.chengdu.cn/1700001')
response_data.encoding='utf-8'

# Re_find_time_taoge2 = re.compile(
#         ur'\d{4}?([年|\/|\/|\.|\s|\-]*?)\d{1,2}([月|\/|\/|\.|\s|\-]*?)\d{1,2}([日|\/|\/|\.|\s|\-]*?)\s*?\d{1,2}([\:|时|\-]*?)\d{1,2}([\:|分|\-]*?)\d{1,2}([\:|秒|\-]?)')


Re_find_time_taoge2 = re.compile(
        ur'\d{4}?[年|\/|\/|\.|\s|\-]*?\d{1,2}[月|\/|\/|\.|\s|\-]*?\d{1,2}[日|\/|\/|\.|\s|\-]*?\s*?\d{1,2}[\:|时|\-]*?\d{1,2}[\:|分|\-]*?\d{1,2}[\:|秒|\-]?')

# Re_find_time_ll=re.compile(r'(\d{4}[年]?\d{2][月]?\d{2}[日]?\s.*?\d{1,2}[时|\:|\-]?\d{1,2}[分|\:|\-]?\d{1,2}[秒]?)|(\d{4}[\-]\d{2][\-]\d{2}[\-]\s.*?\d{1,2}[时|\:|\-]?\d{1,2}[分|\:|\-]?\d{1,2}[秒]?)')

Re_find_time_ll=re.compile(r'\d{4}([年|\/|\/|\.|\s|\-]*?)\d{1,2}\1\d{1,2}\s\d{1,2}([\:|\-]*?)\d{1,2}\2\d{1,2}')





test='123456asdqwertasdasdasdaaaaaaaaaaaa123456asd123456asdasdasd123456'
Re_find_time=re.compile(r'\d{4}([\:|\/|\-])\d{2}\1')
test2='2017-12-11 11:11:11             2017-11-11 11:11:11   2017-11/11 11H11M11s  2017/11/11 11:11:11'
print Re_find_time.findall(test2)


# print Re_find_time_ll.findall(response_data.text)
#
# print Re_find_time_taoge2.findall(response_data.text)


