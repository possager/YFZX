#_*_coding:utf-8_*_
import scrapy
import time
import re
import json

class taihainet(scrapy.Spider):
    name = 'taihainet'
    urls=['http://app.taihainet.com/?app=mobile&controller=list&jsoncallback=json&catid=101&contentid=20']
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        for url_to_visit in self.urls:
            yield scrapy.Request(url=url_to_visit,headers=headers,cookies={},meta={'contentid':10})

    def deal_index(self,response):

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

        # thisurl = response.url
        # thisurl_split = thisurl.split('contentid=')
        # nexturl = thisurl_split[0] + 'contentid=' + str(int(thisurl_split[1] + 20))

        taihainet_contentid=20
        response_body=response.body.split('(')[1].split(')')[0]
        datajson= json.loads(response_body)
        datajson_data=datajson['data']
        for one_index in datajson_data:
            id= one_index['contentid']
            if int(one_index['contentid'])>taihainet_contentid:
                taihainet_contentid=int(one_index['contentid'])
            title= one_index['title']
            url= one_index['url']
            thisindex={
                'id':id,
                'title':title,
                'url':url
            }
            yield scrapy.Request(url=url,meta={'data':thisindex,'contentid':taihainet_contentid},cookies=cookies,headers=headers)
        thisurl=response.url
        thisurl_split=thisurl.split('contentid=')
        nexturl=thisurl_split[0]+'contentid='+str(taihainet_contentid+20)

        if taihainet_contentid > response.meta['contentid']:
            yield scrapy.Request(url=nexturl,meta={'contentid':taihainet_contentid},headers=headers,cookies=cookies)

    def deal_content(self,response):
        print response.body
        #--------------------------------!
        #这里没有处理对应的content,此外,这个网站没有对应的评论.
        #--------------------------------!