# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import re
from scrapy.exceptions import IgnoreRequest
from YFZX.persionalSetting import Exam_exist
import scrapy
from scrapy.exceptions import CloseSpider
from YFZX.proxy_to_redis import get_proxy_from_redis
from YFZX.examing_redis import change
# import threading



from scrapy import signals
import hashlib
from YFZX.page_filter import path_to_redis



class YfzxSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class responseToWhereMiddleware(object):
    def process_request(self, request, spider):


        #添加的判断是否重复功能的模块
        # if request.meta['plant_form']!='None':
        #     url_request=request.url
        #     hash_url=str(hashlib.md5(url_request).hexdigest())
        #     thisclass=path_to_redis()
        #     num_result=thisclass.examing(url_to_exam=request.url,plantform=request.meta['plant_form'])
        #     num_exist= thisclass.redis.get(str(request.meta['plant_form']+request.meta['plant_form']))#这里没有使用change函数转到相应的键值对,是因为这里就直接以网站的plant_from来作为键值对的名字的
        #     # print num_exist
        #     if num_exist is not None and int(num_exist)>100:
        #         # raise CloseSpider()
        #         # return IgnoreRequest
        #         num_plant_form = change(request.meta['plant_form'])
        #         thisclass.redis.set(num_plant_form+num_plant_form,0)
        #         raise CloseSpider()
        #         # request.callback=spider.close
        #         # return request
        #     if num_result==0:
        #         num_plant_form = change(request.meta['plant_form'])
        #         thisclass.redis.incr(num_plant_form+num_plant_form)
        #         num_exist = thisclass.redis.get(num_plant_form+num_plant_form)
        #         print request.url,'has been crawled'
        #         # raise IgnoreRequest()#已经爬去过了

        Re_pattern_newssc_index = re.compile(r'\bhttp://.*?\.newssc\.org/\B')  # 不知道为什么这里的\b和\B作用刚好相反,可能雨scrapy有关
        Re_pattern_newssc_news = re.compile(r'\bhttp://.*?\.newssc\.org/system/\d{8}/\d{9}.html')
        Re_pattern_chengdu_news=re.compile(r'http://.*?chengdu\.cn/\d{4}/\d{4}/\d{7}.*?')
        Re_pattern_chengdu_index=re.compile(r'')
        Re_pattern_sohudetail=re.compile(r'm.sohu.com/\w/\d.*?')
        Re_pattern_toutiao_detail=re.compile(r'')
        Re_pattern_xinhuanet_content=re.compile(r'xinhuanet.com/[a-z]*?/\d{4}-\d{2}/\d{2}/c_\d*?.htm')#http://m.news.cn/ent/2017-06/30/c_1121238259.htm
        Re_pattern_taihainet=re.compile(r'm.taihainet.com/(lifeid|news)/.*?/.*?/(\d{4}-\d{2}-\d{2}|\d*?)/\d*?.htm')#http://m.taihainet.com/news/twnews/latq/2017-07-06/2031222.htm



        print request.url
        if 'newssc' in request.url:
            if 'http://www.newssc.org/' == request.url:
                request.callback=spider.deal_index_from_webpage
            elif 'newssc.org' in request.url:

                url_otherHomepage = Re_pattern_newssc_index.findall(string=request.url)  # 找出所有不是具体新闻的链接继续跟进访问.
                url_News = Re_pattern_newssc_news.findall(string=request.url)

                if url_otherHomepage:
                    request.callback = spider.deal_content_from_news
                elif url_News:
                    request.callback = spider.deal_content_from_news
                else:
                    raise IgnoreRequest



        elif 'wap.chengdu.cn' in request.url:
            request.callback=spider.deal_content
        elif 'sohu.com' in request.url:
            if 'api.m.sohu.com' in request.url:
                request.callback=spider.deal_index
            elif 'sohu.com/a/' in request.url:
                request.callback=spider.deal_content2
            elif Re_pattern_sohudetail.findall(request.url):
                request.callback=spider.SomeOneNewsDeal
            elif 'http://v2.sohu.com/public-api/feed?' in request.url:
                request.callback=spider.deal_index2
            elif 'm.sohu.com/reply/api/comment/list/cursor?newsId' in request.url:
                request.callback=spider.commentDeal
            elif 'https://apiv2.sohu.com/api/comment/list?page_size=10&topic_id' in request.url:##7-20发现漏掉链接
                request.callback=spider.deal_comment2
                print request.url
            elif 'http://apiv2.sohu.com/api/topic/load?page_size=10&topic_source_id=' in request.url:#7-20日发现这个url在每次请求评论的时候会出现在第一次的请求中.
                request.callback=spider.deal_comment3
        elif 'panda.qq.com' in request.url:
            if '//panda.qq.com/cd/interface/topic/' in request.url and 'pagesize' in request.url:
                request.callback=spider.deal_index
            elif '//panda.qq.com/cd/interface/topic/getThreadByTid?s_code=&tid=' in request.url:
                request.callback=spider.deal_content
            elif '//panda.qq.com/cd/interface/topic/getRepliesByTid?s_code=&tid=' in request.url:
                request.callback=spider.deal_comment
        elif 'www.toutiao.com' in request.url:
            if '//www.toutiao.com/api/pc/feed/' in request.url:
                request.callback=spider.deal_index
            elif '//www.toutiao.com/group/' in request.url:
                request.callback=spider.deal_content
            elif 'http://www.toutiao.com/api/comment/list/?group_id=' in request.url:
                request.callback=spider.deal_comment
        elif 'wa.news.cn' in request.url or 'xinhuanet' in request.url or 'news.xinhuanet.com' in request.url or 'http://comment.home.news.cn/a/newsCommAll.do?_ksTS=' in request.url:
            Re_result=Re_pattern_xinhuanet_content.findall(request.url)
            # if Re_result:
            #     request.callback=spider.deal_content
            if '//qc.wa.news.cn/nodeart/list?nid=' in request.url:
                request.callback=spider.deal_index
            elif Re_pattern_xinhuanet_content.findall(request.url):
                request.callback = spider.deal_content
            elif 'http://comment.home.news.cn/a/newsCommAll.do?_ksTS=' in request.url:
                request.callback=spider.deal_comment
        elif 'taihainet.com' in request.url:
            if 'http://app.taihainet.com/?app=mobile&controller=list' in request.url:
                request.callback=spider.deal_index
            elif request.url=='http://m.taihainet.com/news/':
                request.callback=spider.getID_from_mainpage
            elif Re_pattern_taihainet.findall(request.url):
                request.callback=spider.deal_content
        elif 'thepaper.cn' in request.url:
            if '//m.thepaper.cn/channel_' in request.url:
                request.callback=spider.deal_index
            elif 'http://m.thepaper.cn/load_channel.jsp?nodeids=' in request.url:
                request.callback=spider.deal_content
        elif 'xilu' in request.url:
            if 'm.xilu.com/list' in request.url or 'm.xilu.com/index.html' in request.url:
                request.callback=spider.deal_index
            elif 'http://m.xilu.com/v/' in request.url:
                request.callback=spider.deal_content
        # elif 'xinhuanet' in request.url:
        #     if
        else:
            print '#########################################################################'
            print '          W      R     O      N      G      IN     middleware'
            print '          the url is ---',request.url
            print '#########################################################################'


class HttpProxyMiddleware(object):
    def process_request(self,request,spider):
        # thread1=threading.Thread(target=)
        # if 'sohu' not in request.url:
        #     try:
        #         proxy_ip='http://'+get_proxy_from_redis()
        #         request.meta['proxy']=proxy_ip
        #         print 'set proxy successfully'
        #     except Exception as e:
        #         print e
        #
        pass

class refuseMiddleware(object):
    def process_spider_input(self,response,spider):
        if response.status in [400,403,404]:#这里还缺少一个url被404的次数
            return response.request