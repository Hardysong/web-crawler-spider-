# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from tutorial.items import DmozItem


class DpSpider(scrapy.spider.Spider):
    name = "dzdp_spider"
    allowed_domains = ["dianping.com"]

    #start_urls = ['http://www.dianping.com/search/category/2/10/r2578p1']
    start_urls = []
    for i in range(1,51):
        start_urls.append('http://www.dianping.com/search/category/2/10/r1495p'+str(i))

    handle_httpstatus_list = [404,403]

    def parse(self,response):
        print '__________'
        if response.status == 403:
            print 'meet 403, sleep 600 sconds'
            import time
            time.sleep(600)
            yield Request(response.url,callback=self.parse)
        #404,页面不存在，直接范围即可
        elif response.status == 404:
            print 'meet 404,return'
        else:
            
            hxs = scrapy.Selector(response)
            xs = hxs.xpath('//*[@id="shop-all-list"]/ul/li')
            for x in xs:
                item = DmozItem()
                #商户名
                name_list = x.xpath('div[2]/div[1]/a[1]/h4/text()').extract()
                name = ''.join(name_list)
                #商户星级
                star_list = x.xpath('div[2]/div[2]/span/@title').extract()
                star_level = ''.join(star_list)
                #商户评论数
                comment = x.xpath('div[2]/div[2]/a[1]/b/text()').extract()
                comment = ''.join(comment)
                #商户地址，进入后获取商户经纬度信息
                dresspath = x.xpath('div[4]/a[1]/@href').extract()
                if not len(dresspath):
                    dresspath = x.xpath('div[3]/a[1]/@href').extract()
                dresspath = ''.join(dresspath)

                #进入dresspath网站，爬取经纬度数据
                next_path = 'http://www.dianping.com' + dresspath
                next_url = next_path[:-7]

                item['title'] = name.encode('gbk')
                item['star'] = star_level.encode('gbk')
                item['comment_num'] = comment.encode('gbk')
                item['link'] = next_url.encode('gbk')
                
                yield Request(next_url,callback=self.parse_location,meta={'item':item})
                
                print name,star_level,comment,next_url,'\n'
            print '__________'

    def parse_location(self,response):
        
        loc_hxs = scrapy.Selector(response)
        loc_xs = loc_hxs.xpath('//div[@id="aside"]/script[1]').extract()[0]
        coord_text = re.findall(r'lng:\w+.\w+,lat:\w+.\w+',loc_xs)[0]

        item = response.meta['item']
        item['location'] = coord_text.encode('gbk')
        return item
        #print  coord_text
