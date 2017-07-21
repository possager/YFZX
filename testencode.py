#_*_coding:utf-8_*_
import random


dict1={}
for i in range(10):
    list1=['div','tag','li','name']
    tag=random.choice(list1)
    try:
        dict1[tag]+=1
    except:
        dict1[tag]=1


print dict1













# reslut= json.loads(json.loads(json.dumps(data_response.text)))
# for url in reslut:
#     print url

