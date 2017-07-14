#_*_coding:utf-8_*_
import scrapy
import re
import json
import time
from YFZX.persionalSetting import Save_result
from YFZX.persionalSetting import Save_org_file




class chinadaily(scrapy.Spider):
    name = 'toutiao'

    def start_requests(self):
        urls = [
            'https://www.toutiao.com/api/pc/feed/?max_behot_time=1499133489&category=__all__&utm_source=toutiao&widen=1&tadrequire=false',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time_tmp=1499131781&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=%E7%BB%84%E5%9B%BE&utm_source=toutiao&as=A1F5F9655ABFB36&cp=595A5F6BB3262E1',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_society&utm_source=toutiao&widen=1&max_behot_time_tmp=1499130277&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_entertainment&utm_source=toutiao&widen=1&max_behot_time_tmp=1499127310&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&mmax_behot_time_tmp=1499126716&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_sports&utm_source=toutiao&widen=1&max_behot_time_tmp=1499129717&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_car&utm_source=toutiao&widen=1&max_behot_time_tmp=1499128582&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_finance&utm_source=toutiao&widen=1&max_behot_time_tmp=1499127720&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=funny&utm_source=toutiao&widen=1&max_behot_time_tmp=1499121867&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_military&utm_source=toutiao&widen=1&max_behot_time_tmp=1499130314&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_fashion&utm_source=toutiao&widen=1&max_behot_time_tmp=1499128255&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_discovery&utm_source=toutiao&widen=1&mmax_behot_time_tmp=1499128281&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_regimen&utm_source=toutiao&widen=1&max_behot_time_tmp=1499128301&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_essay&utm_source=toutiao&widen=1&max_behot_time_tmp=1499125173&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_history&utm_source=toutiao&widen=1&max_behot_time_tmp=1499125194&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_world&utm_source=toutiao&widen=1&max_behot_time_tmp=1499128221&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_travel&utm_source=toutiao&widen=1&max_behot_time_tmp=1499125233&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_baby&utm_source=toutiao&widen=1&max_behot_time_tmp=1499128468&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_story&utm_source=toutiao&widen=1&max_behot_time_tmp=1499125336&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_game&utm_source=toutiao&widen=1&max_behot_time_tmp=1499131054&tadrequire=true',
            # 'https://www.toutiao.com/api/pc/feed/?category=news_food&utm_source=toutiao&widen=1&max_behot_time_tmp=1499128522&tadrequire=true'
        ]
        headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        for url in urls:
            yield scrapy.Request(url=url,headers=headers,cookies={})



    def deal_index(self, response):
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


        datajson_index=json.loads(response.body)
        timestamp=str(int(time.time()))
        thisurl=response.url.split('max_behot_time_tmp=')
        nexturl=thisurl[0]+'max_behot_time_tmp='+timestamp+'&tadrequire=true'
        datajson_index_data=datajson_index['data']
        for one_index in datajson_index_data:
            print one_index
            try:
                title= one_index['title']
            except:
                title=''
            try:
                reply_count= int(one_index['comments_count'])
            except :
                reply_count=0
            url='http://www.toutiao.com'+ one_index['source_url']
            try:
                publish_user= one_index['source']#publisher
            except :
                publish_user=''
            try:
                publish_user_photo=one_index['media_avatar_url']
            except :
                publish_user_photo=''
            id=one_index['group_id']
            print '-----------------------------------------------------------------------------------------------------'
            yield scrapy.Request(url=url,meta={
                'id':id,
                'url':url,
                'reply_count':reply_count,
                'nexturl':nexturl,
                'title':title,
                'publish_user':publish_user,
                'publish_user_photo':publish_user_photo,
                'spider_time':timestamp
            },
                                 headers=headers,
                                 cookies=cookies)


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
        thismeta=response.meta

        data={
            'id':thismeta['id'],
            'url':thismeta['url'],
            'reply_count':thismeta['reply_count'],
            'title':thismeta['title'],
            'publish_user':thismeta['publish_user'],
            'spider_time':thismeta['spider_time'],
            'publish_user_photo':thismeta['publish_user_photo'],
            'content':'',
            'img_urls':[],
            'video_urls':[],
            'publish_time':'',
            'reply_nodes':[],
        }

        #http://www.toutiao.com/api/comment/list/?group_id=6438917736949612802&item_id=6438920814917059074&offset=5&count=15
        if '.toutiao.com' in response.url:
            print response.body
            xpath_data= response.xpath('//div/article/div[1]/h1')
            print response









            #下边都是处理转到对应的评论所需要的信息.
            # Re_content_item_id=re.compile(r'item_id: \'.*?\'')
            # Re_content_qid=re.compile(r'qid : \".*?\"')
            # # print response.body#普通的html文档
            # item_id_re=Re_content_item_id.findall(response.body)
            # print item_id_re
            # if not item_id_re:
            #     qid_re =Re_content_qid.findall(response.body)
            #     print qid_re[0].split('"')[1]#这里的作用是找出文中对应的id部分.
            #     # yield scrapy.Request()
            # else:
            #     print item_id_re[0].split("'")[1]
            #     thisurl=response.url.split('com/a')
            #     #http://www.toutiao.com/api/comment/list/?group_id=
            #     nexturl='http://www.toutiao.com/api/comment/list/?group_id='+thisurl[1].replace('/','')+'&item_id='+str(item_id_re[0].split("'")[1])+'&offset=0&count=20'
            #     yield scrapy.Request(url=nexturl,cookies=cookies,headers=headers,meta={'data':data})


    def deal_comment(self,response):
        thismeta_data=response.meta['data']

        datajson_comment=json.loads(response.body)
        datajson_comment_data_comment=datajson_comment['data']['comments']
        for one_comment in datajson_comment_data_comment:
            content= one_comment['text']#content
            like_count= one_comment['digg_count']#like_count
            publish_time= one_comment['create_time']#publish_time
            id= one_comment['id']#id
            # reply_count= one_comment['reply_count']#reply_count
            publish_user= one_comment['user']['name']#publish_user
            publish_user_photo= one_comment['user']['avatar_url']#publish_user_photo
            publish_user_id= one_comment['user']['user_id']#publish_user_id
            reply_count= one_comment['reply_count']#reply_count
            url = response.url
            reply_nodes = []
            time_format = '’%Y-%m-%d %X'
            spider_time = time.strftime(time_format, time.localtime())
            one_nodes={
                'content':content,
                'like_count':like_count,
                'publish_time':publish_time,
                'id':id,
                'reply_count':reply_count,
                'publish_user':publish_user,
                'publish_user_photo':publish_user_photo,
                'publish_user_id':publish_user_id,
                'url':url,
                'reply_nodes':reply_nodes,
                'spider_time':spider_time
            }
            thismeta_data['reply_nodes'].append(one_nodes)

        Save_result(plantform='toutiao',date_time=response.meta['data']['publish_time'],urlOruid=response.meta['data']['url'],newsidOrtid=response.meta['data']['id'],datatype='news',full_data=response.meta)

        print datajson_comment['data']['total']

