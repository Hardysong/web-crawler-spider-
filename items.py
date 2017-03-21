# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DmozItem(scrapy.Item):
    title = scrapy.Field()
    star = scrapy.Field()
    comment_num = scrapy.Field()
    link = scrapy.Field()
    location = scrapy.Field()

class SoufangItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    latlon = scrapy.Field()
    address = scrapy.Field()
    pro_feature = scrapy.Field()
    belong_region = scrapy.Field()
    huanxian_weizhi = scrapy.Field()
    chanquanmiaoshu = scrapy.Field()
    wuyeleixing = scrapy.Field()
    jungongshijian = scrapy.Field()
    zhandimianji = scrapy.Field()
    dangqihushu = scrapy.Field()
    zonghushu = scrapy.Field()
    lvhualv = scrapy.Field()
    rongjilv = scrapy.Field()
    wuyefei = scrapy.Field()
    kaifashang = scrapy.Field()
    jianzhumianji = scrapy.Field()
