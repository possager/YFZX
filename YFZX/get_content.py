#_*_coding:utf-8_*_
import pymongo
from operator import itemgetter



def getxpath(response_list):


    result_list_PN=sorted(response_list['data'],key=itemgetter('PN'),reverse=True)
    result_list_TL=sorted(response_list['data'],key=itemgetter('TL'),reverse=True)

    result_dict={}
    for i in result_list_PN[0:10]:
        if i['has_url']==0 and i['TL']>1:
            keys1=result_dict.keys()
            if i['xpath'] in keys1:
                result_dict[i['xpath']]+=1
            else:
                result_dict[i['xpath']]=1
    for i in result_list_TL[0:10]:
        keys1=result_dict.keys()
        if i['has_url']==0 and i['TL']>1:
            if i['xpath'] in keys1:
                result_dict[i['xpath']]+=1
            else:
                result_dict[i['xpath']]=1

    # for iii in result_dict.iteritems():
    #     print iii
    #     print len(iii)

    result_dict2=sorted(result_dict.iteritems(),key=lambda x:x[1],reverse=True)

    return result_dict2[0]


if __name__ == '__main__':
    xpath=getxpath('none')
    print xpath