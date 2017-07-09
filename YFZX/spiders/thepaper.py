#_*_coding:utf-8_*_
import scrapy
import time
import re
import json

class thepaper(scrapy.Spider):
    name = 'thepaper'
    urls=[
        'http://m.thepaper.cn/channel_26916',
          # 'http://m.thepaper.cn/channel_25950',
          # 'http://m.thepaper.cn/channel_25951',
          # 'http://m.thepaper.cn/channel_25952',
          # 'http://m.thepaper.cn/channel_25953'
          ]
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Referer':'http://m.xilu.com/index.html',
        'Origin':'http://m.xilu.com',
        'Host':'m.xilu.com',
        }
        for url_to_visit in self.urls:
            yield scrapy.Request(url=url_to_visit,headers=headers,cookies={},meta={})

    def deal_index(self,response):
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



        Re_pattern=re.compile(r'data.*?\:.*?\".*?Math\.random\b')
        re_data=Re_pattern.findall(response.body)
        url_in_content =re_data[0].split('"')[1]
        nexturl='http://m.thepaper.cn/load_channel.jsp?'+url_in_content+str(1)
        # print response.body

        print nexturl
        yield scrapy.Request(url=nexturl,headers=headers,cookies=cookies,meta={'data':{}})

    def deal_content(self,response):
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


        print response.xpath('div/a')##http://m.thepaper.cn/newDetail_commt.jsp?_=1499325674584&contid=1726057对应的评论的格式,评论也是放在对应的div标签中的,