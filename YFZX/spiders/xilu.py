import scrapy
import re
import json
import time

class xilu(scrapy.Spider):
    name = 'xilu'
    urls=[
        'http://m.xilu.com/index.html',
          'http://m.xilu.com/list_1353.html',
          'http://m.xilu.com/list_1283.html',
          'http://m.xilu.com/list_1311.html',
          'http://m.xilu.com/list_1142.html',
          'http://m.xilu.com/list_1412.html',
          'http://m.xilu.com/list_1469.html'
          ]
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
            'X-Requested-With':'XMLHttpRequest'}
        for url_to_visit in self.urls:
            yield scrapy.http.FormRequest(url=url_to_visit,method='post',formdata={'params':{"page":"4"}},headers=headers)

    def deal_index(self, response):

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




        print response.body
        datajson=json.loads(json.dumps(eval(response.body)))
        for one_index in datajson:
            title= one_index['title']#title
            read_count= one_index['onclick']#view
            publish_time= one_index['sdate']#time
            id= one_index['rfilename']#rfilename
            # yield scrapy.Request(url='http://m.xilu.com/v/'+str(id())+'.html',headers=headers,meta={})
            print 'http://m.xilu.com/v/'+str(id)+'.html'
