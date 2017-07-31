#_*_coding:utf-8_*_
import scrapy
from bs4 import BeautifulSoup
import re
import json
import logging
import json
from YFZX import gather_all_funtion
from YFZX.persionalSetting import Save_zip
from YFZX.persionalSetting import Save_org_file
from YFZX.persionalSetting import Save_result
from YFZX import deal_response
from scrapy.exceptions import CloseSpider

import time



#isIndex_request
#plant_form
#download_timeout
#http://wap.chengdu.cn/1700001这个网页有评论，可以找到评论的链接。
#http://changyan.sohu.com/api/2/topic/comments?client_id=cyrHnxhFx&page_size=30&topic_id=630645353&page_no=1

#抓不全，时间寻找出错，有些网页会没有内容，会导致xpath连续错误累计过多，影响后边的内容。


class newssc(scrapy.Spider):
    name = 'chengdu'
    urls=['http://wap.chengdu.cn/'+str(i) for i in range(1696951,1696952)]#1893603#如果超限会返回404错误

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url,meta={'plant_form':'chengdu',
                                               'isIndex_request':True})
    def deal_content(self, response):
        if response.status == 404:
            return#这样设计靠谱吗？

        if response.request.cookies:
            cookies = response.request.cookies
        else:
            cookies = {}
        headers = response.request.headers
        if 'Set-Cookie' in headers.keys():
            print response.headers['Set-Cookie']
            for headers_key in response.headers.keys():
                if 'Set-Cookie' in headers_key:
                    set_cookie = response.headers[headers_key]
                    cookies_name = set_cookie.split(';')[0].split('=')
                    cookies[cookies_name[0]] = cookies_name[1]
                else:
                    headers[headers_key] = response.headers[headers_key]

        data_TCPI=gather_all_funtion.get_result_you_need(response)
        title=data_TCPI[0]
        content=data_TCPI[1]
        img_urls=data_TCPI[3]
        time_format = '%Y-%m-%d'
        spider_time = time.strftime(time_format, time.localtime())

        # try:
        #     publish_time=response.xpath('/html/body/div[4]/div[2]/p/span[4]')
        #     print publish_time
        # except Exception as e:
        #     print e
        #     print 'time wrong'
        publish_time=data_TCPI[2]

        id=str(response.url.split('/')[-1])
        data={
            'url':response.url,
            'content':content,
            'title':title,
            'publish_time':publish_time,
            'img_urls':img_urls,
            'id':id,
            'spider_time':spider_time,
            'reply_node':[]
        }
        # cmt_url='http://changyan.sohu.com/api/2/topic/comments?client_id=cyrHnxhFx&page_size=30&topic_id=630645353&page_no=1'
        Re_find_sid=re.compile(r'sid="\d*?"')
        sid=Re_find_sid.findall(response.body)#为了找到评论
        print sid
        sidnum=sid[0].split('"')[1]

        cmt_url_with_out_num='http://changyan.sohu.com/api/3/topic/liteload?&client_id=cyrHnxhFx&page_size=30&hot_size=5&topic_source_id='
        cmt_url_to_visit=cmt_url_with_out_num+sidnum


        yield scrapy.Request(url=cmt_url_to_visit,headers=headers,cookies=cookies,meta=data)
        # Save_result(plantform='chengdu',date_time=publish_time,urlOruid=response.url,newsidOrtid=id,datatype='news',full_data=data)
        print data


    def deal_comment(self,response):
        datajson=json.loads(response.body)
        datajson_comments=datajson['comments']

        data=response.meta
        comments_data=[]

        if not datajson_comments:
            Save_result(plantform='chengdu', date_time=data['publish_time'], urlOruid=data['url'],
                        newsidOrtid=data['id'], datatype='news', full_data=data)
            return
        else:
            for someone_comment in datajson_comments:
                # id=i['comment_id']
                # content=i['content']
                # publish_time=i['create_time']
                # publish_user=i['passport']['']
                content = someone_comment['content']  # content
                id = someone_comment['comment_id']  # id
                publish_user_photo = someone_comment['passport']['img_url']  # publish_user_photo
                publish_user = someone_comment['passport']['nickname']  # publish_user
                publish_user_id = someone_comment['passport']['user_id']  # publish_user_id
                create_time = someone_comment['create_time']  # publish_time
                spider_time = time.time()

                thiscomments = {
                    'content': content,
                    'id': id,
                    'publish_user_photo': publish_user_photo,
                    'publish_user': publish_user,
                    'publish_user_id': publish_user_id,
                    'create_time': create_time,
                    'spider_time': spider_time
                }
                comments_data.append(thiscomments)
            data['reply_node']=comments_data


        Save_result(plantform='chengdu',date_time=data['publish_time'],urlOruid=data['url'],newsidOrtid=data['id'],datatype='news',full_data=data)
