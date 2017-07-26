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



#抓不全，时间寻找出错，有些网页会没有内容，会导致xpath连续累计过多，影响后边的内容。


class newssc(scrapy.Spider):
    name = 'chengdu'
    urls=['http://wap.chengdu.cn/'+str(i) for i in range(1696951,3000000)]#1893603#如果超限会返回404错误

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url,meta={'plant_form':'chengdu',
                                               'isIndex_request':True})
    def deal_content(self, response):
        if response.status == 404:
            return CloseSpider()

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
        Save_org_file(plantform='chengdu',date_time=publish_time,urlOruid=response.url,newsidOrtid=id,datatype='news',full_data=response.body)
        Save_zip(plantform='chengdu',date_time=publish_time,urlOruid=response.url,newsidOrtid=id,datatype='news')
        Save_result(plantform='chengdu',date_time=publish_time,urlOruid=response.url,newsidOrtid=id,datatype='news',full_data=data)
        print data
