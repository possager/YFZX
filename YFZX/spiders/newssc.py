import scrapy
import re
import time

class newssc(scrapy.Spider):
    name = 'newssc'
    urls=['http://www.newssc.org/']
    def start_requests(self):
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        }
        for url in self.urls:
            yield scrapy.Request(url=url,headers=headers,meta={'plant_form':'None'})

    def deal_index_from_webpage(self,response):
        Re_find_news_url=re.compile(r'href=".*?"')
        url_find_by_re_list=Re_find_news_url.findall(response.body)
        print url_find_by_re_list
        for url in url_find_by_re_list:
            if 'newssc' in url and '.js' not in url:
                url_split=url.split('"')[1]
                yield scrapy.Request(url=url_split,headers=response.headers,meta={'plant_form':'newssc'})

    def deal_content_from_news(self,response):
        print response.body