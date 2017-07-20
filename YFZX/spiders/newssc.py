import scrapy
import re
import time

class newssc(scrapy.Spider):
    name = 'newssc'
    urls=['']
    def start_requests(self):
        yield scrapy.Request()