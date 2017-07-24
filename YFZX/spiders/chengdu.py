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


#####################chengdu这个是是时间处理模块有问题,问题出在在正文模块中找到对应的时间格式的那部分,总是找不准,导致根据时间来存储数据的模块出了问题7-25
######################这里的redis运作正常,代理运作正常,可以根据需要添加download_timeout参数.
######################在gettitle的模块中有一个问题,是数组取值的时候出现的.





class newssc(scrapy.Spider):
    name = 'chengdu'
    urls=['http://wap.chengdu.cn/'+str(i) for i in range(1696951,3000000)]#1893603#如果超限会返回404错误

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url,meta={'plant_form':'chengdu'})
    def deal_content(self, response):
        if response.status > 400:
            return CloseSpider()
        ##############################################  7-21  ##################
        # content_dict,content_class=deal_response.deal_response(response)
        # DOC_class.insert(content_dict)

        ##############################################  7-21  ##################



        # Re_pattern_index=re.compile(r'\bhttp://.*?\.newssc\.org/\B')#不知道为什么这里的\b和\B作用刚好相反,可能雨scrapy有关
        # Re_pattern_news=re.compile(r'\bhttp://.*?\.newssc\.org/system/\d{8}/\d{9}.html')

        # urllist=self.get_Href_By_Re(response=response)


        # hreflist=response.selector.re(r'href=".*?"')
        # for i in hreflist:
        #     urlinMainPage =i.replace('href=','').replace('"','')
        #     if 'http' in urlinMainPage and 'css' not in urlinMainPage and 'newssc' in urlinMainPage:
        #         yield scrapy.Request(url=urlinMainPage)
                # url_otherHomepage= Re_pattern_index.findall(string=urlinMainPage)#找出所有不是具体新闻的链接继续跟进访问.
                # url_News= Re_pattern_news.findall(string=urlinMainPage)
                # print url_otherHomepage

        # for url_newssc in self.get_Href_By_Re(response=response):
        #     yield scrapy.Request(url=url_newssc)

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


        # try:
        #     publish_time=response.xpath('/html/body/div[4]/div[2]/p/span[4]').extract()[0]+':00'
        # except:
        #     print 'time wrong'

        # title=response.xpath('//div[@class="neirong"]/h2').extract()#body > div.content > div.neirong > h2
        # print title




        data_TCPI=gather_all_funtion.get_result_you_need(response)
        title=data_TCPI[0]
        content=data_TCPI[1]
        # publish_time=data_TCPI[2]
        img_urls=data_TCPI[3]
        time_format = '%Y-%m-%d'
        spider_time = time.strftime(time_format, time.localtime())

        try:
            publish_time=response.xpath('/html/body/div[4]/div[2]/p/span[4]')
            print publish_time
        except Exception as e:
            print e
            print 'time wrong'
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




                # print urlinMainPage
    # def parse_newssc_news_detail(self,response):
    #     print '---------------------------------'
    #     print response.url


        # for mainindex1 in response.selector.css('body > div > div > div > nav > section.nav-port > div.nav-port-o > a'):
        #     url1=mainindex1.css('[href]::attr(href)').extract()[0]
        # for mainindex2 in response.selector.css('body > div > div > div > nav > section.nav-port > div.nav-port-tw > a'):
        #     print mainindex2.css('[href]::attr(href)').extract()[0]
        # for mainindex3 in response.selector.css('body > div > div > div > nav > section.nav-port > div.nav-port-th > a'):
        #     print mainindex3.css('[href]::attr(href)').extract()[0]
        # for mainindex4 in response.selector.css('body > div > div > div > nav > section.nav-port > div.nav-port-fo > a'):
        #     print mainindex4.css('[href]::attr(href)').extract()[0]
    def parse_newssc_news_index(self,response):
        print '======================'
        print response.url


    def parse_chengdu(self,response):
        Re_chengdu_news_index=re.compile(r'http://.*?chengdu\.cn/\d{4}/\d{4}/\d{7}.*?')
        for url_chengdu in self.get_Href_By_Re(response=response,special_words='chengdu'):
            print url_chengdu
            if Re_chengdu_news_index.findall(url_chengdu):
                print url_chengdu
            elif 'news.chengdu.cn' in url_chengdu:
                print url_chengdu.replace(':','&')
            elif Re_chengdu_news_index.findall(url_chengdu):
                print url_chengdu

    def parse_chengdu_news_detail(self,response):
        print response.url







    # def get_Href_By_Re(self,response,special_words):
    #     hreflist = response.selector.re(r'href=".*?"')
    #     for i in hreflist:
    #         urlinMainPage = i.replace('href=', '').replace('"', '')
    #         if 'http' in urlinMainPage and 'css' not in urlinMainPage and special_words in urlinMainPage:
    #             yield urlinMainPage
