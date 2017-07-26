#_*_coding:utf-8_*_
import pymongo
from operator import itemgetter
import redis
import hashlib
from collections import Counter





redis_connect_pool=redis.ConnectionPool(host='localhost',port=6379)
redis1=redis.Redis(connection_pool=redis_connect_pool)#这些配置最好将来全部写到一个模块中去


def getxpath(response_list):


    result_list_PN=sorted(response_list['data'],key=itemgetter('PN'),reverse=True)
    result_list_TL=sorted(response_list['data'],key=itemgetter('TL'),reverse=True)
    #  7-23
    data=response_list['data']
    result_list_TAL=sorted(data,key=itemgetter('TAL'),reverse=True)
    # result_list_ND=sorted(data,key=itemgetter('PN'),reverse=True)#这里改了，在pn里边按照ND的值来排序，因为nd这个指标的误差太大,后来发现还是不行，于是删除了
    # result_list_ND=sorted(result_list_ND,key=itemgetter('ND'),reverse=True)
    # result_list_xpath_x_value=sorted(data,key=itemgetter('xpath_x_value'),reverse=True)
    # result_list_value_of_xpath=sorted(response_list['data'],key=itemgetter('value_of_div_xpath'),reverse=True)#在改了字典的push顺序之后，这里总是出问题。这里边很多问题都是在字典的push
    #顺序改了之后出毛病的


    result_dict={}
    #如果这个指标的比重越大，就是特征越明显，那么取值就越少。
    for i in result_list_PN[0:4]:
        if i['has_url']==0 and i['TL']>1:
            keys1=result_dict.keys()
            if i['xpath'] in keys1:
                result_dict[i['xpath']]+=1
            else:
                result_dict[i['xpath']]=1

    for i in result_list_TL[0:4]:
        keys1=result_dict.keys()
        if i['has_url']==0 and i['TL']>1:
            if i['xpath'] in keys1:
                result_dict[i['xpath']]+=1
            else:
                result_dict[i['xpath']]=1
    # for i in result_list_ND[0:7]:
    #     keys1=result_dict.keys()
    #     if i['has_url']==0 and i['TL']>1:
    #         if i['xpath'] in keys1:
    #             result_dict[i['xpath']]+=1
    #         else:
    #             result_dict[i['xpath']]=1

    if response_list['plant_form'] not in ['newssc']:
        for i in result_list_TAL[0:7]:
            keys1 = result_dict.keys()
            if i['has_url'] == 0 and i['TL'] > 1:
                if i['xpath'] in keys1:
                    result_dict[i['xpath']] += 1
                else:
                    result_dict[i['xpath']] = 1

    # for i in result_list_value_of_xpath[0:7]:
    #     keys1 = result_dict.keys()
    #     if i['has_url'] == 0 and i['TL'] > 1:
    #         if i['xpath'] in keys1:
    #             result_dict[i['xpath']] += 1
    #         else:
    #             result_dict[i['xpath']] = 1

    # for i in result_list_xpath_x_value[0:10]:
    #     keys1 = result_dict.keys()
    #     if i['has_url'] == 0 and i['TL'] > 1:
    #         if i['xpath'] in keys1:
    #             result_dict[i['xpath']] += 1
    #         else:
    #             result_dict[i['xpath']] = 1
    if result_list_PN[0]['has_url']==0 and i['TL']>1:
        result_dict[result_list_PN[0]['xpath']]+=1
    if result_list_TL[0]['has_url']==0 and i['TL']>1:
        result_dict[result_list_TL[0]['xpath']]+=1






    # for iii in result_dict.iteritems():
    #     print iii
    #     print len(iii)

    result_dict2=sorted(result_dict.iteritems(),key=lambda x:x[1],reverse=True)


    if response_list['plant_form'] in ['newssc']:#主要针对四川新闻网的特点来设计的
        if len(result_dict2[0][0].split('/'))>2:
            return result_dict2[0]
        else:
            return result_dict2[1]
    else:
        if len(result_dict2[0][0].split('/'))>2:#注意，这个想四川新闻王的话不能这么用，因为四川新闻网的不懂地区的网页是不一样的，但是url链接却是一样的，用这个会出问题。
           return save_xpath_redis(result_dict2[0],url=response_list['url'],plant_from=response_list['plant_form'])
            # return result_dict2[0]
        else:
            return save_xpath_redis(result_dict2[1],url=response_list['url'],plant_from=response_list['plant_form'])




def save_xpath_redis(xpath_and_tuple,url,plant_from):#判断plantform要么在传入之前判断，要么在传入之后判断//*[@id="page"]/table/tbody/tr[1]/td/table/tbody/tr/td/div/ul[2]/li/table/tbody/tr[4]/td/p[2]
    xpath=xpath_and_tuple[0]
    plant_from=plant_from+'_xpaht100'
    # xpath_hash=hashlib.md5(xpath).hexdigest()
    if redis1.llen(plant_from)<100:
        redis1.rpush(plant_from,xpath)
    else:
        redis1.lpop(plant_from)
        redis1.rpush(plant_from,xpath)

    xpath_list_from_redis=redis1.lrange(plant_from,0,100)
    xpath_set_from_list=set(xpath_list_from_redis)
    dict_xpath={}
    for key in xpath_set_from_list:
        dict_xpath[key]=xpath_list_from_redis.count(key)
    dict_xpath2=sorted(dict_xpath.iteritems(),key=lambda x:x[1],reverse=True)
    # return dict_xpath2
    if len(dict_xpath2[0][0].split('/'))<3:
        try:
            return dict_xpath2[1]
        except Exception as e:
            print e
    else:
        return dict_xpath2[0]



if __name__ == '__main__':
    xpath=getxpath('none')
    print xpath