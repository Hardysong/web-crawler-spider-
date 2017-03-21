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
    
    name = "soufangV2_spider"
    allowed_domains = ["fang.com"]

    #start_urls = ['http://esf.fang.com/housing/0__0_0_0_0_1_0_0/']
    start_urls = []
    for i in range(1,6):
        start_urls.append('http://esf.fang.com/housing/16__0_0_0_0_'+str(i)+'_0_0/')

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
                href = href + 'xiangqing/'

                url = 'http://api.map.baidu.com/geocoder/v2/'
                output = 'json'
                ak = 'i3TSS0YGVZWbEQGev7xRhKeGG2xxUhpv'
                address = address.encode('gbk')
                uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
                temp = urllib.urlopen(uri)
                temp = json.loads(temp.read())

                if temp['status'] == 0:
                    location = temp['result']['location']
                else:
                    location = []

                item['name'] = name.encode('gbk')
                
                item['link'] = href.encode('gbk')
                item['latlon'] = location
                
                yield Request(href,callback=self.parse_detail,meta={'item':item})

                print name
            print '__________'

    def parse_detail(self,response):
        
        loc_hxs = scrapy.Selector(response)
        address = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[1]/text()').extract()
        address = ''.join(address)

        pro_feature = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[2]/text()').extract()
        pro_feature = ''.join(pro_feature)

        belong_region = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[3]/text()').extract()
        belong_region = ''.join(belong_region)

        huanxian_weizhi = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[5]/text()').extract()
        huanxian_weizhi = ''.join(huanxian_weizhi)

        chanquanmiaoshu = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[6]/text()').extract()
        chanquanmiaoshu = ''.join(chanquanmiaoshu)

        wuyeleixing = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[7]/text()').extract()
        wuyeleixing = ''.join(wuyeleixing)

        jungongshijian = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[8]/text()').extract()
        jungongshijian = ''.join(jungongshijian)

        kaifashang = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[9]/text()').extract()
        kaifashang = ''.join(kaifashang)

        jianzhuleibie = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[11]/text()').extract()
        jianzhuleibie = ''.join(jianzhuleibie)

        jianzhumianji = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[12]/text()').extract()
        jianzhumianji = ''.join(jianzhumianji)

        zhandimianji = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[13]/text()').extract()
        zhandimianji = ''.join(zhandimianji)

        dangqihushu = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[14]/text()').extract()
        dangqihushu = ''.join(dangqihushu)

        zonghushu = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[15]/text()').extract()
        zonghushu = ''.join(zonghushu)

        lvhualv = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[16]/text()').extract()
        lvhualv = ''.join(lvhualv)

        rongjilv = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[17]/text()').extract()
        rongjilv = ''.join(rongjilv)

        wuyefei = loc_hxs.xpath('/html/body/div[4]/div[4]/div[1]/div[2]/div[2]/dl/dd[19]/text()').extract()
        wuyefei = ''.join(wuyefei)

        item = response.meta['item']
        item['address'] = address.encode('gbk')
        item['pro_feature'] = pro_feature.encode('gbk')
        item['belong_region'] = belong_region.encode('gbk')
        item['huanxian_weizhi'] = huanxian_weizhi.encode('gbk')
        item['chanquanmiaoshu'] = chanquanmiaoshu.encode('gbk')
        item['wuyeleixing'] = wuyeleixing.encode('gbk')
        item['jungongshijian'] = jungongshijian.encode('gbk')
        item['zhandimianji'] = zhandimianji.encode('gbk')
        item['dangqihushu'] = dangqihushu.encode('gbk')
        item['zonghushu'] = zonghushu.encode('gbk')
        item['lvhualv'] = lvhualv.encode('gbk')
        item['rongjilv'] = rongjilv.encode('gbk')
        item['wuyefei'] = wuyefei.encode('gbk')
        item['kaifashang'] = kaifashang.encode('gbk')
        item['jianzhumianji'] = jianzhumianji.encode('gbk')
        

        return item
