#_*_coding:utf-8_*_
import time
import requests



session1=requests.session()


response_data=session1.request(method='post',url='')





















#
# timedata=time.strptime('2017-07-26 12:40'+':00','%Y-%m-%d %H:%M:%S')
# timestamp=time.mktime(timedata)
# print timestamp
# print timedata


# def is_valid_date(str):
#   '''判断是否是一个有效的日期字符串'''
#   try:
#       timestr=time.strptime(str, "%Y-%m-%d")
#       return timestr
#   except:
#       return False
#
# if __name__ == '__main__':
#     # print 'hellop'
#     # if is_valid_date(str='2017-06-12'):
#     #     print 'hello'
#     # else:
#     #     print 'hello2'
#     print is_valid_date('2017-06-17')