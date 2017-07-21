import scrapy
import json
import time
from YFZX import deal_response





class testStructure(scrapy.Spider):
    name = 'teststructure'
    urls=['http://scnews.newssc.org/system/20170720/000799871.html']

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url)

    # def deal_parse(self,response):
    #     print response.body

    def deal_content_from_news(self,response):
        data_response=deal_response.deal_response(response)
        print data_response