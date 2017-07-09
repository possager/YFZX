#_*_coding:utf-8_*_
import scrapy
import pymongo
import json
import time
import re
from YFZX.items import YfzxItem
from YFZX.items import YfzxCommentItem
from YFZX.persionalSetting import BASIC_FILE
from YFZX.persionalSetting import Save_result
from YFZX.persionalSetting import Save_org_file
from YFZX.persionalSetting import Save_zip
import chardet
import os
import coding
import hashlib



class souhunews(scrapy.Spider):
    name = 'souhu'
    start_urls=['https://api.m.sohu.com/autonews/cpool/?n=%E6%96%B0%E9%97%BB&s=0&c=20&dc=1']


    def parse(self, response):
        print chardet.detect(response.body)
        datajson=json.loads(response.body)
        # print datajson
        for i in datajson['data']['news']:
            # print i['medium_title']#标题
            # print i['view_count']#阅读量
            # print i['media']#发布人
            # print i['created_time']#发布时间
            # print i['comment_count']
            # print i['id']
            yield scrapy.Request(url='https://m.sohu.com/'+str(i['type'])+'/'+str(i['id']),meta={'publish_user':i['media'],
                                                                                                 'title':i['medium_title'],
                                                                                                 'read_count':int(i['view_count']),
                                                                                                 'publish_time':i['created_time'].replace('T',' '),
                                                                                                 'id':i['id'],
                                                                                                 'original_url':response.url,
                                                                                                 })

        urlnext='https://api.m.sohu.com/autonews/cpool/?n=%E6%96%B0%E9%97%BB&s=0&c=20&dc=1'
        urldeal1=urlnext.split('s=')[0]
        urldealnum=urlnext.split('s=')[1].split('&')[0]
        urldeal3=urlnext.split('s=')[1].split('&')[1]
        if int(urldealnum)<950:
            yield urldeal1+str(int(urldealnum)+2)+urldeal3+'&dc=1'

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
        publish_time= response.meta['publish_time']
        read_count=response.meta['read_count']
        newsid=response.meta['id']

        article_content=''

        for content_p in response.xpath('/html/body/section[1]/article/p'):
            try:
                article_content=article_content+content_p.xpath('text()').extract()[0]

                # print chardet.detect(article_content)


            except Exception as e:
                print e
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
                if 'http://s1.rr.itc.cn/p/"images/imgloading.jpg' not in img_url:
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
                                                                                                                                                               'newsid':newsid
                                                                                                                                                               })

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
                                                              'newsid':newsid})
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
        print '----------------------------------------'