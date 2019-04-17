# -*- coding: utf-8 -*-
import scrapy
from ..items import HouseItem
from scrapy import Request
import re


class BaixingSpider(scrapy.Spider):
    name = 'baixing'
    allowed_domains = ['guangzhou.baixing.com']
    start_urls = 'http://guangzhou.baixing.com/zhengzu/?page={page}'
    # script = """
    #         function main(splash)
    #             assert(splash:go(splash.args.url))
    #             splash:runjs("window.scrollTo(0,0.5*document.body.scrollHeight)")
    #             splash:wait(0.5)
    #             splash:runjs("window.scrollTo(0,0.8*document.body.scrollHeight)")
    #             splash:wait(0.5)
    #             return splash:html()
    #         end
    #         """

    def start_requests(self):
        if self.settings.get('CITY') == 'SZ':
            self.start_urls = 'http://shenzhen.baixing.com/zhengzu/?page={page}'
        for i in range(1, self.settings.getint('BAIXING_PAGE')+1):
            yield Request(self.start_urls.format(page=i), callback=self.parse)

    def parse(self, response):
        result = response.xpath('//li[contains(@class,"listing-ad")]')
        for selector in result:
            item = HouseItem()
            try:
                if self.settings.get('CITY') == 'GZ':
                    item['city'] = '广州'
                elif self.settings.get('CITY') == 'SZ':
                    item['city'] = '深圳'
                item['zone'] = selector.xpath('.//div[@class="media-body"]/div[@class="ad-item-detail"][2]/text()').re('\[(\S+?)-')[0]
                item['housearea'] = int(float(selector.xpath('.//div[@class="media-body"]/div[@class="ad-item-detail"][1]/text()').re('([\d.]+)平')[0]))
                item['housetype'] = selector.xpath('.//div[@class="media-body"]/div[@class="ad-item-detail"][1]/text()').extract_first().split('/')[1].strip()
                item['price'] = int(float(selector.xpath('.//span[@class="highlight"]/text()').re('\d+')[0]))
                item['houseurl'] = selector.xpath('.//div[contains(@class,"media-body-title")]/a[1]/@href').extract_first()
                item['per_price'] = int(item['price'] / item['housearea'])
                item['imgurl'] = 'https:'+selector.xpath('.//img/@src').extract_first()
                try:
                    item['housenum'] = int(re.search('(\d+)室', item['housetype']).group(1))
                except:
                    item['housenum'] = 0
            except:
                continue
            yield item

