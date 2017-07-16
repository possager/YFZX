#_*_coding:utf-8_*_
import scrapy
import json
import time
import hashlib
import re
from YFZX.persionalSetting import BASIC_FILE
from YFZX.persionalSetting import Save_result
from YFZX.persionalSetting import Save_org_file


class mycd_qq(scrapy.Spider):
    name = 'mycdqq'
    def start_requests(self):
        headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
                 'Accept':'application/json',
                 'Accept-Encoding':'gzip, deflate, sdch',
                 'Accept-Language':'zh-CN,zh;q=0.8',
                 'Connection':'keep-alive',
                 'Host':'panda.qq.com',
                 'Referer':'http://panda.qq.com/cd/index',
                 'X-Requested-With':'XMLHttpRequest'#关键,没有这个会出现请求过期
                 }
        url='http://panda.qq.com/cd/interface/topic/getRecThreads?s_code=&page=6&pagesize=10'
        yield scrapy.Request(url=url,cookies={'pgv_info':'ssid=s2580718070', 'ts_last':'panda.qq.com/cd/index', 'pgv_pvid':'6693827820', 'ts_uid':'6358905536', 'pgv_pvi':'7088397312', 'pgv_si':'s8851519488'},
                             headers=headers)

    def deal_index(self, response):
        print response.headers
        print response.request.cookies
        response_headrs=response.request.headers


        for headers_key in response.headers.keys():
            # headers_in_index= response.headers
            # if type(response_headrs[headers_key]=='list'):
            response_headrs[headers_key]=response.headers[headers_key]



        # print type(response.headers[headers_key])
        # headers_in_index['Referer']=response.url

        print response_headrs
        response_Json=json.loads(response.body)
        for data_data in response_Json['data']['data']:
            print data_data['favorited']#收藏
            like_count= data_data['favtimes']#like_count
            publish_user_id= data_data['uid']#publish_user_id
            title= data_data['subject']#title
            reply_count= data_data['replies']#reply_count
            publish_time= data_data['pubtime']#publish_time
            read_count= data_data['views']#read_count
            print data_data['shares']#fenxiangshuliang
            publisher_name= data_data['author']['nickname']#publisher_name
            publish_user_photo= data_data['author']['headimgurl']#publish_user_photo
            tid= data_data['tid']#tid
            #http://panda.qq.com/cd/interface/topic/getThreadByTid?s_code=&tid=1033985628517098
            response_headrs['Referer'] = 'http://panda.qq.com/cd/thread/' + str(data_data['tid'])

            yield scrapy.Request(url='http://panda.qq.com/cd/interface/topic/getThreadByTid?s_code=&tid='+str(tid),meta={'like_count':like_count,
                                                                                     'publish_user_id':publish_user_id,
                                                                                     'title':title,
                                                                                     'spider_time':time.time(),
                                                                                     'reply_count':reply_count,
                                                                                     'publish_time':publish_time,
                                                                                     'read_count':read_count,
                                                                                     'publish_user':publisher_name,
                                                                                     'publish_user_photo':publish_user_photo,
                                                                                     'id':tid,
                                                                                    'url':response.url
                                                                                    },headers=response_headrs)
            break


    def deal_content(self,response):
        Save_result(plantform='mycdqq', date_time=response.meta['publish_time'], urlOruid=response.meta['url'],
                    newsidOrtid=response.meta['id'], datatype='news', full_data=response.body)
        headers=response.request.headers
        for i in response.headers:
            headers[i]=response.headers[i]


        print 'in deal_content'
        print response.body
        json_in_content=json.loads(response.body)
        json_in_content_data_post=json_in_content['data']['posts']

        newscontent=''
        img_urls=[]
        for key1 in json_in_content_data_post:
            try:
                json_in_content_data_post_one= json_in_content_data_post[key1]
                for key2 in json_in_content_data_post_one['content']:
                    if key2['type']=='text':
                        # print key2['content']
                        newscontent+=key2['content']
                    else:
                        # print key2['imgurl']
                        # print key2['desc']
                        newscontent+=key2['desc']
                        img_urls.append(key2['imgurl'])
            except Exception as e:
                print e

        reproduce_count=json_in_content['data']['thread']['shares']



        data={}
        for meta_key in response.meta:
            data[meta_key]=response.meta[meta_key]
        data['content']=newscontent
        data['img_urls']=img_urls
        data['reply_nodes']=[]
        data['reproduce_count']=reproduce_count


        url_comment='http://panda.qq.com/cd/interface/topic/getRepliesByTid?s_code=&tid='+response.meta['id']+'&page=1&sort=time&size=20'
        cookiedict=response.request.cookies
        try:
            for cookiekey in response.cookies:
                cookiedict[cookiekey]=response.cookies[cookiekey]
        except Exception as e:
            print e
        yield scrapy.Request(url=url_comment,headers=headers,cookies=cookiedict,meta=data)





    def deal_comment(self,response):
        headers = response.request.headers
        for i in response.headers:
            headers[i] = response.headers[i]


        print response.body
        # print response.body
        print '--------'
        print response.meta
        print '--------'
        json_in_comment=json.loads(response.body)
        json_in_comment_data=json_in_comment['data']
        if json_in_comment_data:
            json_in_comment_data_postreply=json_in_comment_data['postreply']
            for post in json_in_comment_data_postreply:
                content= post['content']#
                like_count= post['favtimes']#like_count
                publish_user_id= post['uid']#publish_user_id
                id= post['tid']#tid
                url= response.url#url
                publish_user= post['author']['nickname']#publish_user
                publish_user_photo= post['author']['headimgurl']#publish_user_photo       maybe is no heading----http://panda.qq.com/static/images/noheadimg.png
                time_format = '’%Y-%m-%d %X'
                spider_time = time.strftime(time_format, time.localtime())#spider_time
                publish_time= post['pubtime']#publish_time
                comment_only_one={
                    'content':content,
                    'publish_user_id':publish_user_id,
                    'like_count':like_count,
                    'id':id,
                    'url':url,
                    'publish_user':publish_user,
                    'publish_user_photo':publish_user_photo,
                    'spider_time':spider_time,
                    'publish_time':publish_time,
                }
                response.meta['reply_nodes'].append(comment_only_one)

            this_comment_url=response.url.split('&page=')
            next_comment_url=this_comment_url[0]+'&page='+str(int(this_comment_url[1].split('&')[0])+1)+'&sort=time&size=20'
            yield scrapy.Request(url=next_comment_url,headers=headers,meta=response.meta)
        else:#请求完成
            resultdict={
                'data':{
                    'like_count':response.meta['like_count'],
                    'content':response.meta['content'],
                    'id':response.meta['id'],
                    'img_urls':response.meta['img_urls'],
                    'publish_time':response.meta['publish_time'],
                    'publish_user_id':response.meta['publish_user_id'],
                    'publish_user_photo':response.meta['publish_user_photo'],
                    'publish_user':response.meta['publish_user'],
                    'read_count':response.meta['read_count'],
                    'reply_count':response.meta['reply_count'],
                    'title':response.meta['title'],
                    'reply_nodes':response.meta['reply_nodes'],
                    'url':response.meta['url'],
                    'reproduce_count':response.meta['reproduce_count'],
                    'spider_time':response.meta['spider_time']
                    # 'read_count':response.meta['read_count'],


                }
            }
            result_json=json.dumps(resultdict)
            Save_result(plantform='mycdqq',date_time=response.meta['publish_time'],urlOruid=response.meta['url'],newsidOrtid=response.meta['id'],datatype='news',full_data=resultdict)

