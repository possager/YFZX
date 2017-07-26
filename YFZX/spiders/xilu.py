#_*_coding:utf-8_*_
import scrapy
import re
import json
import time
from YFZX import gather_all_funtion
from YFZX import persionalSetting
#这个网站在对应板块的url被访问完的时候，会返回空的列表[]
#这个网站是有评论的。。。。。。。。。。。。。
#http://changyan.sohu.com/api/2/topic/comments?callback=jQuery17008864328161226998_1500974781673&client_id=cysYw3AKM&page_size=30&topic_id=3527226100&page_no=1&_=1500974781966
#http://changyan.sohu.com/api/2/topic/comments?callback=jQuery170016130385152918425_1500974409334&client_id=cysYw3AKM&page_size=30&topic_id=3463438994&page_no=1&_=1500974409535


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
            for i in range(0,300):
                time.sleep(1)
                yield scrapy.http.FormRequest(url=url_to_visit,method='post',formdata={'params':{"page":str(i)}},headers=headers,meta={'plant_form':'None',
                                                                                                                                       'isIndex_request':True})

    def deal_index(self, response):
        print response.body

        # json_charge=json.loads('['+response.body.split('[')[1].split(']')[0]+']')
        json_charge=json.loads(json.dumps(eval(response.body)))
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
                'plant_form':'xilu',
                'isIndex_request':False
            })

    def deal_content(self,response):

        data_TCPI=gather_all_funtion.get_result_you_need(response)
        print data_TCPI
        content=data_TCPI[1]
        data=response.meta
        data['content']=content
        #发现发布时间里边有'刚刚，1小时前，2小时前，3小时前'
        publish_time=response.meta['data']['publish_time']
        if publish_time==u'刚刚':
            publish_time=time.time()
        elif u'小时前' in publish_time:
            time_pass=int(publish_time.replace(u'小时前',''))*60*60
            publish_time=time.time()-time_pass
        elif u'分钟前' in publish_time:
            time_pass=int(publish_time.replace(u'分钟前',''))*60
            publish_time=time.time()-time_pass
        elif '-' in publish_time and len(publish_time)==5:
            publish_time='2017-'+publish_time

        persionalSetting.Save_org_file(plantform='xilu', date_time=publish_time,
                                       urlOruid=response.meta['data']['url'],
                                       newsidOrtid=response.meta['data']['id'], datatype='news',
                                       full_data=response.body)
        persionalSetting.Save_zip(plantform='xilu',date_time=publish_time,urlOruid=response.meta['data']['url'],
                                       newsidOrtid=response.meta['data']['id'],datatype='news')


        #http://changyan.sohu.com/api/3/topic/liteload?&client_id=cysYw3AKM&page_size=30&hot_size=10&topic_source_id=1000010001000523
        cmt_url_without_id='http://changyan.sohu.com/api/3/topic/liteload?&client_id=cysYw3AKM&page_size=30&hot_size=10&topic_source_id='
        this_page_id=response.url.split('/')[-1].split('.')[0]
        cmt_url=cmt_url_without_id+this_page_id
        yield scrapy.Request(url=cmt_url,headers=response.headers)

#http://changyan.sohu.com/api/2/topic/comments?page_size=30&topic_id=3527226100&page_no=2
    def deal_comment(self,response):
        print response.body
        # persionalSetting.Save_result(plantform='xilu', date_time=response.meta['data']['publish_time'],
        #                              urlOruid=response.meta['data']['url'],
        #                              newsidOrtid=response.meta['data']['id'], datatype='news', full_data=response.meta['data'])