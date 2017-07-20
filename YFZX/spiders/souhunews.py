#_*_coding:utf-8_*_
import scrapy
import json
import time
import re
from YFZX.items import YfzxItem
from YFZX.items import YfzxCommentItem
from YFZX.persionalSetting import BASIC_FILE
from YFZX.persionalSetting import Save_result
from YFZX.persionalSetting import Save_org_file
from YFZX.persionalSetting import Save_zip
from YFZX import gather_all_funtion
from scrapy.exceptions import CloseSpider
import chardet
import os
import coding
import hashlib


class souhunews(scrapy.Spider):
    name = 'sohu'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
    }

    def start_requests(self):
        headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
                }
        # urls = ['https://api.m.sohu.com/autonews/cpool/?n=%E6%96%B0%E9%97%BB&s=0&c=20&dc=1']#'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=8&page=9&size=20'
        urls=['http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=8&page=1&size=20',
              'https://api.m.sohu.com/autonews/cpool/?n=%E6%96%B0%E9%97%BB&s=0&c=20&dc=1']
        for url in urls:
            yield scrapy.Request(url=url,headers=headers,meta={'plant_form':'None'})

    # def parse(self, response):
    #     print response.body


    def deal_index(self, response):
        print chardet.detect(response.body)
        datajson=json.loads(response.body)
        # print datajson
        for i in datajson['data']['news']:
            yield scrapy.Request(url='https://m.sohu.com/'+str(i['type'])+'/'+str(i['id']),meta={'publish_user':i['media'],
                                                                                                 'title':i['medium_title'],
                                                                                                 'read_count':int(i['view_count']),
                                                                                                 'publish_time':i['created_time'].replace('T',' '),
                                                                                                 'id':i['id'],
                                                                                                 'original_url':response.url,
                                                                                                 'plant_form':'sohu'
                                                                                                 })

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
        }
        # urlnext='https://api.m.sohu.com/autonews/cpool/?n=%E6%96%B0%E9%97%BB&s=0&c=20&dc=1'
        urlnext=response.url
        urldeal1=urlnext.split('s=')[0]

        urldealnum=urlnext.split('s=')[1].split('&')[0]
        print urldealnum
        urldeal3=urlnext.split('s=')[1].split('&')[1]
        if int(urldealnum)<950:
            urlnext=urldeal1+'s='+str(int(urldealnum)+1)+'&'+urldeal3+'&dc=1'
            yield scrapy.Request(url=urlnext,headers=headers,meta={'plant_form':'None'})
            print 'sucessfully yield----',urlnext


    def deal_index2(self,response):
        data_json=json.loads(response.body)
        if not data_json:
            return
        for data_in_json in data_json:
            publish_user=data_in_json['authorName']
            title=data_in_json['title']
            id=data_in_json['id']
            publish_user_id=data_in_json['authorId']
            publish_time=data_in_json['publicTime']
            publish_time=int(publish_time) / 1000

            time_format = '%Y-%m-%d'
            publish_time_stamp_9 = time.localtime(float(publish_time))
            publish_time = time.strftime(time_format, publish_time_stamp_9)

            urlnext='http://m.sohu.com/a/'+str(id)+'_'+str(publish_user_id)
            yield scrapy.Request(url=urlnext,headers=self.headers,meta={'data':{
                'publish_user':publish_user,
                'title':title,
                'id':id,
                'publish_user_id':publish_user_id,
                'publish_time':publish_time
            },
            'plant_form':'sohu',
            'publish_time':publish_time,
            'id':id,
            'publish_user':publish_user,
            'title':title})
        url_this_index=response.url.split('page=')
        url_next_index=url_this_index[0]+'page='+str(int(url_this_index[1].split('&')[0])+1)+'&size=20'
        print url_next_index
        yield scrapy.Request(url=url_next_index,headers=self.headers,meta={'plant_form':'None'})


    def SomeOneNewsDeal(self,response):
        # try:
        #     print response.xpath('/html/body/section[1]/article/h1/text()').extract()[0]
        # except Exception as e:
        #     print e
        Save_org_file(plantform='sohu',date_time=response.meta['publish_time'],urlOruid=response.url,newsidOrtid=response.meta['id'],datatype='news',full_data=response.body)
        Save_zip(plantform='sohu', date_time=response.meta['publish_time'], urlOruid=response.url,
                 newsidOrtid=response.meta['id'], datatype='news')

        url= response.url
        publish_user= response.meta['publish_user']
        title= response.meta['title']
        time_format = '’%Y-%m-%d %X'
        # spider_time = time.strftime(time_format, time.localtime())  # spider_time
        # publish_time = post['pubtime']  # publish_time
        # publish_time= time.strftime(time_format,response.meta['publish_time'])
        publish_time=response.meta['publish_time']
        read_count=response.meta['read_count']
        newsid=response.meta['id']

        article_content=''

        for content_p in response.xpath('/html/body/section[1]/article/p'):
            try:
                article_content=article_content+content_p.xpath('text()').extract().pop()

                # print chardet.detect(article_content)


            except Exception as e:
                print e
                print 'wrong in get content'
        time_format='’%Y-%m-%d %X'
        spider_time=time.strftime(time_format,time.localtime())
        # print spider_time
        article= response.xpath('/html/body/section[1]/article').extract()
        Re_panttern_findimg=re.compile(r'<img src=".*?>')
        # aritcle_crude=article
        imgsrclist2=[]
        for article_crude in article:
            imgsrc_list=Re_panttern_findimg.findall(article_crude)
            for img_url in imgsrc_list:
                if 'http://s1.rr.itc.cn/p/images/imgloading.jpg' not in img_url:
                    if 'http' in img_url:
                        imgsrclist2.append(img_url.split('"')[1])
                    else:
                        imgsrclist2.append('https:'+img_url.split('"')[1])
        content={}
        data={}
        data['publish_user']=publish_user
        data['url']=url
        data['title']=title



        data['publish_time']=publish_time
        data['read_count']=read_count
        data['spider_time']=spider_time
        data['content']=article_content
        print chardet.detect(article_content.encode('utf-8'))
        data['img_urls']=imgsrclist2
        data['reply_nodes']=[]
        content['data']=data
        datajson=json.dumps(content)
        # print datajson

        thisclass=YfzxItem()
        thisclass['content']=datajson
        thisclass['_id']='souhu'
        thisclass['update_time']=time.time()

        yield scrapy.Request('https://m.sohu.com/reply/api/comment/list/cursor?newsId='+str(response.meta['id'])+'&pageSize=15&preCursor=0&isLogin=true',meta={'publish_user':publish_user,
                                                                                                                                                               'url':url,
                                                                                                                                                               'title':title,
                                                                                                                                                               'publish_time':publish_time,
                                                                                                                                                               'read_count':read_count,
                                                                                                                                                               'spider_time':spider_time,
                                                                                                                                                               'content':content,
                                                                                                                                                               'img_urls':imgsrclist2,
                                                                                                                                                               'data':data,
                                                                                                                                                               'newsid':newsid,
                                                                                                                                                               'plant_form':'None'
                                                                                                                                                               })

    def deal_content2(self,response):
        # print response.url
        Save_org_file(plantform='sohu', date_time=response.meta['publish_time'], urlOruid=response.url,
                      newsidOrtid=response.meta['id'], datatype='news', full_data=response.body)
        Save_zip(plantform='sohu', date_time=response.meta['publish_time'], urlOruid=response.url,
                 newsidOrtid=response.meta['id'], datatype='news')


        data_TCPI=gather_all_funtion.get_result_you_need(response)
        content=data_TCPI[1]
        # publish_time=data_TCPI[2]
        img_urls=data_TCPI[3]
        # time_format = '%Y-%m-%d'
        # spider_time = time.strftime(time_format, time.localtime())
        # publish_time=time.strftime(time_format,time.localtime(float(response.meta['publish_time'])))

        # print response.body
        data=response.meta['data']
        data['content']=content
        data['reply_nodes']=[]
        data['img_urls']=img_urls




        Re_find_comment_id=re.compile(r'cms_id: \'.*?\'')
        try:
            comment_id=Re_find_comment_id.findall(response.body)
            print content
            print '\n'
            print data_TCPI[0]
            comment_id_find_by_re=comment_id[0]
            comment_id_find_by_re=comment_id_find_by_re.split("\'")[1]
            #https://apiv2.sohu.com/api/comment/list?page_size=10&topic_id=3500748995&page_no=2
            url_to_comments='https://apiv2.sohu.com/api/comment/list?page_size=10&topic_id='+str(comment_id_find_by_re)+'&page_no=2'
            yield scrapy.Request(url=url_to_comments,headers=response.headers,meta={'plant_form':'None',
                                                                                    'data':data
                                                                                    })
        except Exception as e:
            print e

        # yield scrapy.Request(url='None')


    def commentDeal(self,response):

        contentdict={}
        # thiscommentLastId=None
        preCommentDict=response.meta['data']
        newsid=response.meta['newsid']
        # contentdict['data']={}
        thiscommentList = []


        #因为这里的回复结构是倒叙的
        def getOneComment(comment):#调整回复的结构
            thiscommentdict={}
            # thiscommentdict['content'] =comment['content'].encode('utf-8')
            thiscommentdict['content'] =comment['content']
            thiscommentdict['like_count']= comment['support_count']  # 赞成数
            print comment['comments']  # 是否有自评论
            thiscommentdict['id']= comment['comment_id']  # 言论id
            thiscommentdict['publish_time']= comment['create_time']  #
            thiscommentdict['reply_count']= len(comment['comments'])
            thiscommentdict['publish_user']= comment['passport']['nickname']
            thiscommentdict['url']= response.url
            thiscommentdict['sonid'] =comment['reply_id']#父贴id
            thiscommentList.append(thiscommentdict)
        #     for childcomment in comment['comments']:
        #         getOneComment(childcomment)
        #
        # def reply_Structure(reply_dict_list):
        #     dict1=reply_dict_list.pop()
        #     if reply_dict_list:
        #         dict1['reply_nodes']=reply_Structure(reply_dict_list)
        #     else:
        #         dict1['reply_nodes']=[]
        #     return dict1

        dataunicode = unicode(response.body, encoding='GBK', errors='ignore')#处理编码
        # dataunicode=dataunicode.encode('utf-8')
        dataunicode=dataunicode.encode('utf-8')
        datajson = json.loads(dataunicode)
        if datajson['data']['comments']:#看评论回复是不是空的,空的很有可能就是爬完了,跳到存储模块
            for jsoncomments in datajson['data']['comments']:
                getOneComment(jsoncomments)
                if len(thiscommentList)>1:
                    contentdict['data']=thiscommentList.pop()
                    contentdict['data']['reply_nodes'] = []
                    contentdict['data']['reply_count']=len(thiscommentList)+1
                    # contentdict['data']['reply_nodes'].append(reply_Structure(thiscommentList))#后边要求不要这个模块

                elif len(thiscommentList)==1:#这里处理的都是某一个评论,最终都将会汇聚到一个list中
                    contentdict['data']=thiscommentList.pop()
                    contentdict['data']['reply_nodes']=[]
                else:
                    contentdict['data']=[]
                thiscommentList=[]
                preCommentDict['reply_nodes'].append(contentdict['data'])
                preCommentDict['newsid']=newsid
                # commentjson=json.dumps(contentdict)#这是某一个评论的,现在做成json还早了点
                # print commentjson
                # thiscommentList['']

            try:
                thiscommentLastId=datajson['data']['comments'][-1]['comment_id']
                print response.url
                # https://m.sohu.com/reply/api/comment/list/cursor?newsId=498936235&pageSize=15&preCursor=0&isLogin=true
                commenturlnowSplit = response.url.split('preCursor=')
                commenturlnext = commenturlnowSplit[0] + 'preCursor=' + str(thiscommentLastId) + '&'+commenturlnowSplit('&')[1]
                yield scrapy.Request(url=commenturlnext,meta={'data':preCommentDict,
                                                              'newsid':newsid,
                                                              'plant_form':'None'})
            except Exception as e:
                print e,'wrong1'





            # commentdata=unicode(response.body,encoding='GBK',errors='ignore')
            # commentjson=json.loads(commentdata)
            # # print commentjson
            # if commentjson['data']['comments']:
            #
            #     for i in commentjson['data']['comments']:
            #         for j in i:
            #             if j==u'from':
            #                 print i['from']
            #                 pass
            #             else:
            #                 print i[j]
            #         thisid=i['comment_id']
            #
            #
            #         print thisid
                    # yield thisclassx




        else:
            Save_result(plantform='sohu',date_time=response.meta['publish_time'],urlOruid=response.meta['url'],newsidOrtid=response.meta['newsid'],datatype='news',full_data={'data':response.meta['data']})

            # thiscommentfile=BASIC_FILE+'/搜狐新闻/speeches/'+str(response.meta['publish_time'].split(' ')[0])
            # if os.path.exists(thiscommentfile):
            #     with open(thiscommentfile+'/'+'Sohu_'+str(int(time.mktime(time.strptime(response.meta['publish_time'],'%Y-%m-%d %H:%M:%S'))))+str(hashlib.md5(response.url).hexdigest())+'_'+str(response.meta['newsid']),'w+') as cmfl:
            #         # cmfl.write(str(preCommentDict))
            #         json.dump({'data':response.meta['data']},cmfl)
            # else:
            #     os.makedirs(thiscommentfile)
            #     with open(thiscommentfile+str('/'+'Sohu_'+str(int(time.mktime(time.strptime(response.meta['publish_time'],'%Y-%m-%d %H:%M:%S'))))+'_'+str(hashlib.md5(response.url).hexdigest())+'_'+str(response.meta['newsid'])),'w+') as cmfl:
            #         # cmfl.write(json.loads(preCommentDict))
            #         json.dump({'data':response.meta['data']},cmfl)
            # Save_zip(plantform='sohu',date_time=response.meta['publish_time'],urlOruid=response.meta['url'],newsidOrtid=response.meta['newsid'],datatype='news')
        print '----------------------------------------'

    # def close(spider, reason):
    #     raise CloseSpider('nothing')


    def deal_comment2(self,response):#处理https://apiv2.sohu.com/api/comment/list?这样的url返回的评论
        try:
            data_json = json.loads(response.body)
            if data_json['jsonObject']['error_code']:
                return scrapy.Request(url='http://apiv2.sohu.com/api/topic/load?page_size=10&topic_source_id=502873239&page_no=1&hot_size=5',meta={'plant_form':'None'})
        except Exception as e:
            # yield scrapy.Request(url='http://apiv2.sohu.com/api/topic/load?page_size=10&topic_source_id=502873239&page_no=1&hot_size=5')
            pass
            try:
                data_json=json.loads(response.body.split('(')[1].split(')')[0])
            except Exception as e:
                # print response.body
                return

        reply_nodes=[]
        print data_json
        for comment in data_json['jsonObject']['comments']:
            publish_user=comment['passport']['nickname']
            publish_user_id=comment['passport']['user_id']
            publish_time=comment['create_time']
            publish_user_photo=comment['passport']['img_url']
            content=comment['content']
            reply_count=comment['reply_count']
            url=response.url
            id=comment['comment_id']
            child_node={
                'publish_user':publish_user,
                'publish_user_id':publish_user_id,
                'publish_time':publish_time,
                'publish_user_photo':publish_user_photo,
                'content':content,
                'reply_count':reply_count,
                'url':url,
                'id':id
            }
            response.meta['data']['reply_nodes'].append(child_node)


    def deal_comment3(self,response):#这里的评论处理是最后一个的时候,在其他的处理模块里都处理不了的时候才处理的,
        #要注意的是,现在一共返现了3个comment评论的来源链接
        try:
            thiscommentList=[]
            data_json=json.loads(response.body)
            if not data_json['jsonObject']['comments']:
                print 'no informathion in comment3'
                return
            for comment in data_json['jsonObject']['comments']:
                comment['content'] = comment['content']
                comment['like_count'] = comment['support_count']  # 赞成数
                print comment['comments']  # 是否有自评论
                comment['id'] = comment['comment_id']  # 言论id
                comment['publish_time'] = comment['create_time']  #
                comment['reply_count'] = len(comment['comments'])
                comment['publish_user'] = comment['passport']['nickname']
                comment['url'] = response.url
                comment['sonid'] = comment['reply_id']  # 父贴id
                thiscommentList.append(comment)
            data=response.meta
            data['reply_nodes'].append(data)

#http://apiv2.sohu.com/api/topic/load?page_size=10&topic_source_id=502873239&page_no=1&hot_size=5
            url_this_comment=response.url.split('page_no=')
            url_next_comment=url_this_comment[0]+'page_no='+str(int(url_this_comment[1].split('&')[0])+1)+'&'+url_this_comment[1].split('&')[1]
            print url_next_comment
            yield scrapy.Request(url=url_next_comment,meta={'data':data})
        except Exception as e:
            print e
            return