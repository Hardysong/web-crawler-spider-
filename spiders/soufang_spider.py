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
    
    name = "soufang_spider"
    allowed_domains = ["fang.com"]

    #start_urls = ['http://esf.fang.com/housing/0__0_0_0_0_1_0_0/']
    start_urls = []
    for i in range(1,1):
        start_urls.append('http://esf.fang.com/housing/1__0_0_0_0_'+str(i)+'_0_0/')

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

            for i in range(1,21):
                item = SoufangItem()
                
                n = "%02d" % i
                houselist = 'houselist_B09_' + n
                
                name_ = hxs.xpath('//*[@id="' + houselist + '"]/dl/dd/p[1]/a/text()').extract()
                name = ''.join(name_)
            
                type_ = hxs.xpath('//*[@id="' + houselist + '"]/dl/dd/p[1]/span/text()').extract()
                build_type = ''.join(type_)
            
                region_1 = hxs.xpath('//*[@id="' + houselist + '"]/dl/dd/p[2]/a[1]/text()').extract()
                region_2 = hxs.xpath('//*[@id="' + houselist + '"]/dl/dd/p[2]/a[2]/text()').extract()
                region1 = ''.join(region_1)
                region2 = ''.join(region_2)
                region = region1 + '_'+region2
            
                address_ = hxs.xpath('//*[@id="' + houselist + '"]/dl/dd/p[2]/text()').extract()
                address = ''.join(address_)
                address = address.split('-')[-1]
                address = address.strip()

                on_sell_ = hxs.xpath('//*[@id="' + houselist + '"]/dl/dd/ul/li[1]/a/text()').extract()
                on_sell = ''.join(on_sell_)

                on_rent_ = hxs.xpath('//*[@id="' + houselist + '"]/dl/dd/ul/li[2]/a/text()').extract()
                on_rent = ''.join(on_rent_)

                year_ = hxs.xpath('//*[@id="' + houselist + '"]/dl/dd/ul/li[3]/text()').extract()
                year = ''.join(year_)

                unit_price_ = hxs.xpath('//*[@id="' + houselist + '"]/div/p[1]/span[1]/text()').extract()
                unit_price = ''.join(unit_price_)
 
                http = hxs.xpath('//*[@id="' + houselist + '"]/dl/dd/p[1]/a/@href').extract()
                href = ''.join(http)

                url = 'http://api.map.baidu.com/geocoder/v2/'
                output = 'json'
                ak = 'hcKAyA267aaroS6MycGoecsospPrxMkA'
                address = address.encode('gbk')
                uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
                temp = urllib.urlopen(uri)
                temp = json.loads(temp.read())

                if temp['status'] == 0:
                    location = temp['result']['location']
                else:
                    location = []

                item['name'] = name.encode('gbk')
                item['build_type'] = build_type.encode('gbk')
                item['region'] = region.encode('gbk')
                item['address'] = address
                item['on_sell'] = on_sell.encode('gbk')
                item['on_rent'] = on_rent.encode('gbk')
                item['build_year'] = year.encode('gbk')
                item['unit_price'] = unit_price.encode('gbk')
                item['link'] = href.encode('gbk')
                item['latlon'] = location
                
                yield Request(href,callback=self.parse_detail,meta={'item':item})

                print name,build_type,region,address,on_sell,on_rent,year,unit_price,href,location
            print '__________'

    def parse_detail(self,response):
        
        loc_hxs = scrapy.Selector(response)
        build_num_ = loc_hxs.xpath('/html/body/div[3]/div[4]/div[1]/div[2]/div[2]/ul/li[2]/text()').extract()
        build_num = ''.join(build_num_)

        total_households_ = loc_hxs.xpath('/html/body/div[3]/div[4]/div[1]/div[2]/div[2]/ul/li[4]/text()').extract()
        total_households = ''.join(total_households_)

        plot_ratio_ = loc_hxs.xpath('/html/body/div[3]/div[4]/div[1]/div[2]/div[2]/ul/li[6]/text()').extract()
        plot_ratio = ''.join(plot_ratio_)

        green_ratio_ = loc_hxs.xpath('/html/body/div[3]/div[4]/div[1]/div[2]/div[2]/ul/li[8]/text()').extract()
        green_ratio = ''.join(green_ratio_)

        property_fee_ = loc_hxs.xpath('/html/body/div[3]/div[4]/div[1]/div[2]/div[2]/ul/li[10]/text()').extract()
        property_fee = ''.join(property_fee_)

        item = response.meta['item']
        item['build_num'] = build_num.encode('gbk')
        item['total_households'] = total_households.encode('gbk')
        item['plot_ratio'] = plot_ratio.encode('gbk')
        item['greening_ratio'] = green_ratio.encode('gbk')
        item['properity_fee'] = property_fee.encode('gbk')

        return item
