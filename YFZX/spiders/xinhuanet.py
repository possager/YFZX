#_*_coding:utf-8_*_
import json
import re
import time
import scrapy
from YFZX.persionalSetting import Save_result



class xinhuanet(scrapy.Spider):
    name = 'xinhuanet'
    urls=[
        'http://qc.wa.news.cn/nodeart/list?nid=113353&pgnum=2&cnt=12',#新闻
        # 'http://qc.wa.news.cn/nodeart/list?nid=11145724&pgnum=2&cnt=12',#全球
        # 'http://qc.wa.news.cn/nodeart/list?nid=11145721&pgnum=3&cnt=12',#财经
        # 'http://qc.wa.news.cn/nodeart/list?nid=11145727&pgnum=2&cnt=12',#娱乐
        # 'http://qc.wa.news.cn/nodeart/list?nid=11145722&pgnum=3&cnt=12',#照片
        # 'http://qc.wa.news.cn/nodeart/list?nid=11145737&pgnum=2&cnt=12',#社区
    ]
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        for url in self.urls:
            yield scrapy.Request(url=url,headers=headers,cookies={})




    def deal_index(self, response):
        if response.request.cookies:
            cookies=response.request.cookies
        else:
            cookies={}
        headers=response.request.headers
        if 'Set-Cookie' in headers.keys():
            print response.headers['Set-Cookie']
            for headers_key in response.headers.keys():
                if 'Set-Cookie' in headers_key:
                    set_cookie=response.headers[headers_key]
                    cookies_name=set_cookie.split(';')[0].split('=')
                    cookies[cookies_name[0]]=cookies_name[1]
                else:
                    headers[headers_key]=response.headers[headers_key]

        response_body= response.body.replace('(','').replace(')','')

        datajson_index=json.loads(response_body)
        datajson_index_data_list=datajson_index['data']['list']
        for one_index in datajson_index_data_list:
            # nodeid=one_index['NodeId']
            id= one_index['DocID']#id
            title= one_index['Title']#title
            publish_time= one_index['PubTime']#publish_time
            url= one_index['LinkUrl']#url
            # publish_user= one_index['Editor']#publish_user
            publish_user= one_index['SourceName']
            thisindex={
                'id':id,
                'title':title,
                'url':url,
                'publish_time':publish_time,
                'publish_user':publish_user,
                'content':'',#很多内容在这里没有填.后边补充
                'reply_nodes':[]
}
            thismeta={'data':thisindex}
            yield scrapy.Request(url=url, headers=headers, cookies=cookies,meta=thismeta)

    def deal_content(self,response):
        if response.request.cookies:
            cookies=response.request.cookies
        else:
            cookies={}
        headers=response.request.headers
        if 'Set-Cookie' in headers.keys():
            print response.headers['Set-Cookie']
            for headers_key in response.headers.keys():
                if 'Set-Cookie' in headers_key:
                    set_cookie=response.headers[headers_key]
                    cookies_name=set_cookie.split(';')[0].split('=')
                    cookies[cookies_name[0]]=cookies_name[1]
                else:
                    headers[headers_key]=response.headers[headers_key]



        #--------------------------------!
        #这里缺少对应的内容提取模块
        thismeta=response.meta
        pass#
        thisurl=response.url#http://news.xinhuanet.com/politics/2017-07/06/c_1121271022.htm
        thisurl_split=thisurl.split('c_')
        thisurl_split_id=thisurl_split[1].split('.')[0]#http://comment.home.news.cn/a/newsCommAll.do?_ksTS=1499304714&callback=json&newsId=1-129435368&pid=2
        nexturl_timestamp=str(int(time.time()))
        nexturl='http://comment.home.news.cn/a/newsCommAll.do?_ksTS='+nexturl_timestamp+'&callback=json&newsId=1-'+thisurl_split_id+'&pid=1'
        yield scrapy.Request(url=nexturl,cookies=cookies,headers=headers,meta=thismeta)
        #--------------------------------!

    def deal_comment(self,response):
        if response.request.cookies:
            cookies=response.request.cookies
        else:
            cookies={}
        headers=response.request.headers
        if 'Set-Cookie' in headers.keys():
            print response.headers['Set-Cookie']
            for headers_key in response.headers.keys():
                if 'Set-Cookie' in headers_key:
                    set_cookie=response.headers[headers_key]
                    cookies_name=set_cookie.split(';')[0].split('=')
                    cookies[cookies_name[0]]=cookies_name[1]
                else:
                    headers[headers_key]=response.headers[headers_key]



        thismeta=response.meta

        datajson_original=response.body.split('(')[1].split(')')[0]
        datajson=json.loads(datajson_original)
        for one_comment in datajson['contentAll']:
            id= one_comment['commentId']#id
            publish_user_photo= one_comment['userImgUrl']#publish_user_photo
            publish_user= one_comment['nickName']#publish_user
            publish_time= one_comment['commentTime']#publis_time
            content= one_comment['content']#content
            publish_user_id= one_comment['userId']#publish_user_id
            like_count= one_comment['upAmount']#like_count
            reply_count= len(one_comment['parent'])#reply_count
            url= response.url#url
            reply_nodes=[]
            video_urls= one_comment['videoUrl']#video_urls
            for reply_one_node in one_comment['parent']:
                reply_node_id = reply_one_node['commentId']  # id
                reply_node_publish_user_photo = reply_one_node['userImgUrl']  # publish_user_photo
                reply_node_publish_user = reply_one_node['nickName']  # publish_user
                reply_node_publish_time = reply_one_node['commentTime']  # publis_time
                reply_node_content = reply_one_node['content']  # content
                reply_node_publish_user_id = reply_one_node['userId']  # publish_user_id
                reply_node_like_count = reply_one_node['upAmount']  # like_count
                # reply_node_reply_count = len(reply_one_node['parent'])  # reply_count
                reply_node_url = response.url  # url
                reply_node_video_urls = reply_one_node['videoUrl']  # video_urls
                reply_node_reply_nodes=[]
                thisreply_node = {
                    'id': id,
                    'publish_user_photo': reply_node_publish_user_photo,
                    'publish_user': reply_node_publish_user,
                    'publish_time': reply_node_publish_time,
                    'content': reply_node_content,
                    'publish_user_id': reply_node_publish_user_id,
                    'like_count': reply_node_like_count,
                    # 'reply_count': reply_node_reply_count,
                    'url': reply_node_url,
                    'video_urls': reply_node_video_urls,
                    'reply_nodes':reply_node_reply_nodes
                }
                reply_nodes.append(thisreply_node)



            thiscomment={
                'id':id,
                'publish_user_photo':publish_user_photo,
                'publish_user':publish_user,
                'publish_time':publish_time,
                'content':content,
                'publish_user_id':publish_user_id,
                'like_count':like_count,
                'reply_count':reply_count,
                'url':url,
                'video_urls':video_urls,
                'reply_nodes':reply_nodes
            }
            thismeta['data']['reply_nodes'].append(thiscomment)
        if len(datajson['contentAll'])>9:
            thisurl=response.url
            thisurl_split=thisurl.split('pid=')
            next_url=thisurl_split[0]+'pid='+str(int(thisurl_split[1])+1)
            yield scrapy.Request(url=next_url,meta=thismeta,cookies=cookies,headers=headers)
        else:
            Save_result(plantform='xinhuanet',date_time=response.meta['data']['publish_time'],urlOruid=response.meta['data']['url'],newsidOrtid=response.meta['data']['id'],datatype='news',full_data={'data':thismeta['data']})