# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YfzxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id=scrapy.Field()
    content=scrapy.Field()
    update_time=scrapy.Field()

class YfzxCommentItem(scrapy.Item):
    like_count=scrapy.Field()
    publish_user_id=scrapy.Field()
    reply_count=scrapy.Field()
    content=scrapy.Field()
    url=scrapy.Field()
    publish_user=scrapy.Field()
    publish_user_photo=scrapy.Field()
    ancestor_id=scrapy.Field()
    spider_time=scrapy.Field()
    publish_time=scrapy.Field()
    id=scrapy.Field()
    dislike_count=scrapy.Field()
    read_count=scrapy.Field()

