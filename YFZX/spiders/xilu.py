#_*_coding:utf-8_*_
import scrapy
import re
import json
import time
from YFZX import gather_all_funtion
from YFZX import persionalSetting
#这个网站在对应板块的url被访问完的时候，会返回空的列表[]

class xilu(scrapy.Spider):
    name = 'xilu'
    urls=[
          'http://m.xilu.com/index.html',
          'http://m.xilu.com/list_1353.html',
          'http://m.xilu.com/list_1283.html',
          'http://m.xilu.com/list_1311.html',
          'http://m.xilu.com/list_1142.html',
          # 'http://m.xilu.com/list_1412.html'#这个是解析图片，估计会出现解析不准确的情况。
          'http://m.xilu.com/list_1469.html'
          ]
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
            'X-Requested-With':'XMLHttpRequest',#重要
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'m.xilu.com',
            'Upgrade-Insecure-Requests':'1'

        }
        for url_to_visit in self.urls:
            for i in range(0,100):
                yield scrapy.http.FormRequest(url=url_to_visit,method='post',formdata={'params':{"page":"50"}},headers=headers,meta={'plant_form':'None'})

    def deal_index(self, response):
        json_charge=json.loads(response.body)
        if not json_charge:
            return

        if response.request.cookies:
            cookies = response.request.cookies
        else:
            cookies = {}
        headers = response.request.headers
        if 'Set-Cookie' in response.headers.keys():
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
        del (headers['X-Requested-With'])

        for one_index in datajson:
            title= one_index['title']#title
            read_count= one_index['onclick']#view
            publish_time= one_index['sdate']#time
            id= one_index['rfilename']#rfilename

            # headers['GET']='/v/'+str(id)+'.html'
            url_page='http://m.xilu.com/v/'+str(id)+'.html'
            # yield scrapy.Request(url=url_page,headers=headers,meta={'data':{
            #     'title':title,
            #     'read_count':read_count,
            #     'publish_time':publish_time,
            #     'id':id
            # }})
            # print 'http://m.xilu.com/v/'+str(id)+'.html'

            yield scrapy.http.FormRequest(url=url_page,method='post',headers=headers,meta={
                'data':{
                    'title':title,
                    'read_count':read_count,
                    'publish_time':publish_time,
                    'id':id,
                    'url':url_page
                },
                'plant_form':'xilu'
            })

    def deal_content(self,response):
        persionalSetting.Save_org_file(plantform='xilu',date_time=response.meta['data']['publish_time'],urlOruid=response.meta['data']['url'],
                                       newsidOrtid=response.meta['data']['id'],datatype='news',full_data=response.body)
        data_TCPI=gather_all_funtion.get_result_you_need(response)
        print data_TCPI
        content=data_TCPI[1]
        data=response.meta
        data['content']=content
        persionalSetting.Save_result(plantform='xilu',date_time=response.meta['data']['publish_time'],urlOruid=response.meta['data']['url'],
                                       newsidOrtid=response.meta['data']['id'],datatype='news',full_data=data)
        persionalSetting.Save_zip(plantform='xilu',date_time=response.meta['data']['publish_time'],urlOruid=response.meta['data']['url'],
                                       newsidOrtid=response.meta['data']['id'],datatype='news')