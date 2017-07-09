#_*_coding:utf-8_*_
import scrapy
from bs4 import BeautifulSoup
import re
import json
import logging
import json


class YFZX(scrapy.Spider):
    name = 'YFZX'
    start_urls=['http://wap.chengdu.cn/']


    def parse(self,response):
        print 'In parse default'
    def parse_newssc(self, response):
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

        for url_newssc in self.get_Href_By_Re(response=response):
            yield scrapy.Request(url=url_newssc)




                # print urlinMainPage
    def parse_newssc_news_detail(self,response):
        print '---------------------------------'
        print response.url


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







    def get_Href_By_Re(self,response,special_words):
        hreflist = response.selector.re(r'href=".*?"')
        for i in hreflist:
            urlinMainPage = i.replace('href=', '').replace('"', '')
            if 'http' in urlinMainPage and 'css' not in urlinMainPage and special_words in urlinMainPage:
                yield urlinMainPage
