import scrapy
import json
import time
from YFZX import deal_response
from YFZX import get_content
import re




class testStructure(scrapy.Spider):
    name = 'teststructure'
    # urls=['http://scnews.newssc.org/system/20170720/000799871.html']
    # urls=['http://lz.newssc.org/system/20170720/002229987.html']
    urls=['http://leshan.newssc.org/system/20170718/002228105.html']
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url,meta={'plant_form':'newssc'})

    # def deal_parse(self,response):
    #     print response.body

    def deal_content_from_news(self,response):
        data_response_dict,data_response=deal_response.deal_response(response)
        get_content.getxpath(data_response_dict)