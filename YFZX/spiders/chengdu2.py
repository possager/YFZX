import scrapy
import time


class chengdu2(scrapy.Spider):
    name = 'chengdu2'
    urls = ['http://wap.chengdu.cn/' + str(i) for i in range(1696951, 1696952)]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url,meta={'plant_form':'chengdu'})

    def deal_content(self,response):
        # title=response.xpath('/html/body/div[3]/div[2]/h2/text()').extract()
        # content=''
        # for content_text in response.xpath('/html/body/div[3]/div[2]/article/p/text()').extract():
        #     content+=content_text
        # publish_time=response.xpath('/html/body/div[4]/div[2]/p/span[4]')
        # pass
        # class_webpage=response.xpath('/html/body')
        # for webpage in class_webpage:
        #     print webpage.xpath('@class').extract()
        class_webpage=response.xpath('/html/body/div[3]/@class').extract()
        print class_webpage