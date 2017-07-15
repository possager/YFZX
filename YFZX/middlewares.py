# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import re
from scrapy.exceptions import IgnoreRequest

import scrapy
from spiders import chengdu


from scrapy import signals


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

        Re_pattern_newssc_index = re.compile(r'\bhttp://.*?\.newssc\.org/\B')  # 不知道为什么这里的\b和\B作用刚好相反,可能雨scrapy有关
        Re_pattern_newssc_news = re.compile(r'\bhttp://.*?\.newssc\.org/system/\d{8}/\d{9}.html')
        Re_pattern_chengdu_news=re.compile(r'http://.*?chengdu\.cn/\d{4}/\d{4}/\d{7}.*?')
        Re_pattern_chengdu_index=re.compile(r'')
        Re_pattern_sohudetail=re.compile(r'm.sohu.com/\w/\d.*?')
        Re_pattern_toutiao_detail=re.compile(r'')
        Re_pattern_xinhuanet_content=re.compile(r'xinhuanet.com/[a-z]*?/\d{4}-\d{2}/\d{2}/c_\d*?.htm')#http://m.news.cn/ent/2017-06/30/c_1121238259.htm
        Re_pattern_taihainet=re.compile(r'm.taihainet.com/(lifeid|news)/.*?/.*?/(\d{4}-\d{2}-\d{2}|\d*?)/\d*?.htm')#http://m.taihainet.com/news/twnews/latq/2017-07-06/2031222.htm



        print request.url
        if 'http://www.newssc.org/' == request.url:
            request.callback=spider.parse_newssc
        elif 'newssc.org' in request.url:

            url_otherHomepage = Re_pattern_newssc_index.findall(string=request.url)  # 找出所有不是具体新闻的链接继续跟进访问.
            url_News = Re_pattern_newssc_news.findall(string=request.url)

            if url_otherHomepage:
                request.callback = spider.parse_newssc_news_detail
            elif url_News:
                request.callback = spider.parse_newssc_news_index
            else:
                raise IgnoreRequest






# class toWhichParseMiddleware(object):
#     def process_request(self, request, spider):
#         Re_pattern_newssc_index=re.compile(r'\bhttp://.*?\.newssc\.org/\B')#不知道为什么这里的\b和\B作用刚好相反,可能雨scrapy有关
#         Re_pattern_newssc_news=re.compile(r'\bhttp://.*?\.newssc\.org/system/\d{8}/\d{9}.html')
#         url_otherHomepage = Re_pattern_newssc_news.findall(string=request.url)  # 找出所有不是具体新闻的链接继续跟进访问.
#         url_News = Re_pattern_newssc_news.findall(string=request.url)
#         if url_otherHomepage:
#             request.callback=spider.parse_newssc_news_detail
#         elif url_News:
#             request.callback=spider.parse_newssc_news_index

        elif 'wap.chengdu.cn' in request.url:
            request.callback=spider.deal_content
        # elif 'chengdu.cn' in request.url:

            # request.callback=spider.parse_chengdu_news_detail


        elif 'api.m.sohu.com/autonews' in request.url:
            request.callback=spider.parse
        elif Re_pattern_sohudetail.findall(request.url):
            request.callback=spider.SomeOneNewsDeal
        elif 'm.sohu.com/reply/api/comment/list/cursor?newsId' in request.url:
            request.callback=spider.commentDeal
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
        elif 'qc.wa.news.cn' in request.url or 'news.xinhuanet.com' in request.url or 'http://comment.home.news.cn/a/newsCommAll.do?_ksTS=' in request.url:
            Re_result=Re_pattern_xinhuanet_content.findall(request.url)
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
        else:
            print '#########################################################################'
            print '          W      R     O      N      G      IN     middleware'
            print '          the url is ---',request.url
            print '#########################################################################'