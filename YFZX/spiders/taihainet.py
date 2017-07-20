#_*_coding:utf-8_*_
import scrapy
import time
import re
import json
from YFZX import gather_all_funtion
from YFZX import persionalSetting



class taihainet(scrapy.Spider):
    name = 'taihainet'
    #http://m.taihainet.com/news/
    #http://app.taihainet.com/?app=mobile&controller=list&jsoncallback=json&catid=100&contentid=40
    urls=['http://m.taihainet.com/news/']
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        for url_to_visit in self.urls:
            yield scrapy.Request(url=url_to_visit,headers=headers,cookies={},meta={'contentid':1000000000})

    def getID_from_mainpage(self,response):
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
        Re_find_id_in_mainPage=re.compile(r'id\:.*?\,')
        web_id=Re_find_id_in_mainPage.findall(response.body)[0].replace('id:','').replace(',','')
        pass
        yield scrapy.Request(url='http://app.taihainet.com/?app=mobile&controller=list&jsoncallback=json&catid=100&contentid='+web_id,cookies=cookies,headers=headers,meta={'contentid':int(web_id)})

    def deal_index(self,response):
        print response.meta['contentid']

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

        taihainet_contentid=response.meta['contentid']
        response_body=response.body.split('(')[1].split(')')[0]
        try:
            datajson= json.loads(response_body)
        except Exception as e:
            print e
            return
        datajson_data=datajson['data']
        for one_index in datajson_data:
            id= one_index['contentid']
            # if int(one_index['contentid'])<taihainet_contentid:
            #     taihainet_contentid=int(one_index['contentid'])
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
        nexturl=thisurl_split[0]+'contentid='+str(taihainet_contentid-40)

        # if taihainet_contentid > response.meta['contentid'] or taihainet_contentid<2000000:
        if taihainet_contentid > 100:
            yield scrapy.Request(url=nexturl,meta={'contentid':taihainet_contentid},headers=headers,cookies=cookies)
        else:
            # print response.meta['contentid']
            print taihainet_contentid
            print '------------------------------------------------!'

    def deal_content(self,response):#台海网有下一页,此功能代码还没有设计
        # print response
        data=gather_all_funtion.get_result_you_need(response)
        # for element in gather_all_funtion
        content=data[1]
        # imglist=data[1]
        # publish_user=response.xpath('/html/body/div[3]/span[2]/span/a')#没有抓取到发帖人,后边单独写一个模块
        time_format = '%Y-%m-%d'
        spider_time = time.strftime(time_format, time.localtime())
        publish_time=data[2]
        img_urls=data[3]

        if len(publish_time.split(':'))==2:
            publish_time+=':00'
        else:
            print publish_time
            publish_time='2211-11-11 11:11:11'



        data={}
        data['url']=response.url
        data['title']=response.meta['data']['title']
        data['id']=response.meta['data']['id']
        data['url']=response.meta['data']['url']
        data['spider_time']=spider_time
        data['img_urls']=img_urls
        data['publish_time']=publish_time
        # data['publish_user']=publish_user
        data['content']=content






        print '\n\n'
        persionalSetting.Save_org_file('taihainet',date_time=data['publish_time'],urlOruid=data['url'],newsidOrtid=data['id'],datatype='news',full_data=response.body)
        persionalSetting.Save_result(plantform='taihainet',date_time=data['publish_time'],urlOruid=data['url'],newsidOrtid=data['id'],datatype='news',full_data={'data':data})
        #--------------------------------!
        #这里没有处理对应的content,此外,这个网站没有对应的评论.
        #--------------------------------!