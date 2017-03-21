# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import urllib
import urllib2
import json

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from tutorial.items import SoufangItem

class SfSpider(scrapy.spider.Spider):
    
    name = "lianjia_spider"
    #allowed_domains = ["bj.lianjia.com/"]

    #start_urls = ['http://esf.fang.com/housing/0__0_0_0_0_1_0_0/']
    start_urls = []
    for i in range(1,71):
        start_urls.append('http://bj.lianjia.com/xiaoqu/haidian/pg'+str(i)+'/')

    handle_httpstatus_list = [404,403]

    def parse(self,response):
        reload(sys)
        sys.setdefaultencoding('utf8')

        print '__________'
        if response.status == 403:
            print 'meet 403, sleep 600 sconds'
            import time
            time.sleep(1200)
            yield Request(response.url,callback=self.parse)
        #404,页面不存在，直接范围即可
        elif response.status == 404:
            print 'meet 404,return'
        else:
            
            hxs = scrapy.Selector(response)

            for i in range(1,31):
                item = SoufangItem()
                
                
                name_ = hxs.xpath('/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[1]/a/text()').extract()
                name = ''.join(name_)

                http = hxs.xpath('/html/body/div[4]/div[1]/ul/li['+str(i)+']/div[1]/div[1]/a/@href').extract()
                href = ''.join(http)
                #href = href + 'xiangqing/'

                item['name'] = name.encode('gbk')
                
                item['link'] = href.encode('gbk')

                yield Request(href,callback=self.parse_detail,meta={'item':item})

                print name, href
            print '__________'

    def parse_detail(self,response):
        #print 'in'

        loc_hxs = scrapy.Selector(response)
        loudongzongshu = loc_hxs.xpath('/html/body/div[5]/div[2]/div[2]/div[5]/span[2]/text()').extract()
        loudongzongshu = ''.join(loudongzongshu)

        fangwuzongshu = loc_hxs.xpath('/html/body/div[5]/div[2]/div[2]/div[6]/span[2]/text()').extract()
        fangwuzongshu = ''.join(fangwuzongshu)

        item = response.meta['item']
        item['address'] = loudongzongshu.encode('gbk')
        item['zonghushu'] = fangwuzongshu.encode('gbk')

        return item
